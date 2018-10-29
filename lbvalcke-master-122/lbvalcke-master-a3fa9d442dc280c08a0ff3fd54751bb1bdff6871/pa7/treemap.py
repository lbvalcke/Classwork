# CS 121: Drawing TreeMaps
# Author: Luis Buenaventura Valcke (UCID 438594)
#

import sys
import csv
import json

from drawing import ChiCanvas, ColorKey


MIN_RECT_SIDE=0.01
MIN_RECT_SIDE_FOR_TEXT=0.03
X_SCALE_FACTOR=12
Y_SCALE_FACTOR=10


def calc_weights(t):
    '''
    Recursively edits the weights of tree nodes based on the values
    of its respective leaves. 

    Inputs:
        t: a tree
    '''    
    
    # Checks to see if it received a leaf
    if t.get_children_as_list() == [] and t.weight != None:
            return t.weight
    
    # If it receives a node, it tries to process its children and
    # adds the weight of its children to itself 
    elif t.get_children_as_list() != []:
        for child in t.get_children_as_list():
            child_weight = calc_weights(child)
            t.weight += child.weight


def calc_part(t, rect_dict, total, x=0, y=0, bounding_rec_width=1.0, 
              bounding_rec_height=1.0, 
              orientation="horizontal"):
    '''
    Recursively chooses the coordinates of the rectangles based on the 
    weight of each node relative to the weight of the whole tree.
    The coordinates are sliced based on alternating cutting of the provided
    canvas based on the proportional weight of each node. Calls the 
    calc_vert_part function to accomplish vertical cutting while this
    function does the horizontal cutting. It only cuts when it receives a 
    leaf. Returns a dictionary with a list of coordinates and a code for 
    each label. 

    Inputs:
        t: (tree) a tree
        rect_dict: (dictionary) an empty dictionary
        total: (int) the weight of the node of the tree
        x: (float) the left-most x-coordinate bound of the rectangle being constructed
        y: (float) the top-most y-coordinate bound of the rectangle being constructed
        bounding_rec_width: (float) the bounding width of the rectangle
        bounding_rec_height: (float) the bounding range of the rectangle

    Return: Dictionary of lists with the labels as and coordinates and code of
            the rectangle in the list 
    '''
    
    # Checks to see if it received a leaf and bounds its height by the 
    # limit of the respective node
    if t.get_children_as_list() == [] and orientation == "horizontal":
        rect_dict[t.label] = [x, y, 
                              bounding_rec_width, 
                              bounding_rec_height * t.weight / total, 
                              t.code]
        return rect_dict
    elif t.get_children_as_list() == [] and orientation == "vertical":
        rect_dict[t.label] = [x, y, 
                              bounding_rec_width * t.weight / total, 
                              bounding_rec_height, 
                              t.code]
        return rect_dict    
    # If it receives a node it checks if the children are leaves
    elif t.get_children_as_list() != []: 
        for child in t.get_children_as_list():

            # If they are leaves then it calculates 
            # the lists for its respective children 
            # and adds their respective x/y-values 
            # to x/y-value of the next child depending on the cut
            if child.get_children_as_list() == []:
                if orientation == "horizontal":
                    rect_dict = calc_part(child, rect_dict, t.weight, 
                                               x, y, bounding_rec_width, 
                                               bounding_rec_height, 
                                               "vertical")
                    x += rect_dict[child._label][2]
                elif orientation == "vertical":
                    rect_dict = calc_part(child, rect_dict, t._weight, 
                                               x, y, bounding_rec_width, 
                                               bounding_rec_height, 
                                               "horizontal")
                    y += rect_dict[child._label][3]
            # Checks to see if the minimum size of the node
            # is large enough to continue cutting it further
            # if not, it breaks out of the loop and moves to the next node            
            elif child.get_children_as_list() != []:
                if orientation == "horizontal":
                    if bounding_rec_height > MIN_RECT_SIDE:
                        rect_dict = calc_part(child, rect_dict,  
                                               t.weight, x, y, 
                                               bounding_rec_width * child.weight / t.weight, 
                                               bounding_rec_height, 
                                               "vertical")
                        x += bounding_rec_width * child.weight / t.weight
                    
                    else: 
                        rect_dict[t._label] = [x, y, bounding_rec_width, 
                                               bounding_rec_height, 
                                               child.code]
                        x += bounding_rec_width
                        break
                elif orientation == "vertical":
                    if bounding_rec_width > MIN_RECT_SIDE:
                        rect_dict = calc_part(child, rect_dict, 
                                              t.weight, x, y, bounding_rec_width, 
                                              bounding_rec_height * child.weight / t.weight,
                                              "horizontal")
                        y += bounding_rec_height * child.weight / t.weight
                    
                    else:
                        rect_dict[t._label] = [x, 
                                               y, 
                                               bounding_rec_width, 
                                               bounding_rec_height, 
                                               t.code] 
                        y += bounding_rec_height
                        break                    
        return rect_dict
            


def draw_treemap(t, 
                 bounding_rec_height=1.0,
                 bounding_rec_width=1.0,
                 output_filename=None):

    '''
    Draw a treemap and the associated color key

    Inputs:
        t: a tree

        bounding_rec_height: the height of the bounding rectangle.

        bounding_rec_width: the width of the bounding rectangle.

        output_filename: (string or None) the name of a file for
        storing a the image or None, if the image should be shown.
    '''
    
    ### START: DO NOT CHANGE THIS CODE ###
    c = ChiCanvas(X_SCALE_FACTOR, Y_SCALE_FACTOR)

    # define coordinates for the initial rectangle for the treemap
    x_origin_init_rect = 0
    y_origin_init_rect = 0
    height_init_rect = bounding_rec_height
    width_init_rect = bounding_rec_width

    ### END: DO NOT CHANGE THIS CODE ###
     

    ### YOUR CODE HERE ###
    # Calculates the interior weights of the tree, rectangle dictionary,
    # and the color key
    calc_weights(t)
    rect_dict = calc_part(t, {}, t._weight, x_origin_init_rect, 
                               y_origin_init_rect, bounding_rec_width, 
                               bounding_rec_height, "horizontal")
    ck = ColorKey(set([v[4] for v in rect_dict.values()])) 
    
    # Draws the rectangle in the rectangle dictionary
    for key, value in rect_dict.items():
        c.draw_rectangle(value[0], value[1], value[0]+value[2], 
                         value[1]+value[3], fill=ck.get_color(value[4]))

        # Chooses whether it should draw the label based on the size of the
        # rectangle
        if value[2] > MIN_RECT_SIDE_FOR_TEXT and value[3] > MIN_RECT_SIDE_FOR_TEXT:
            # Chooses orientation based on largest measurement
            if value[2] >= value[3]:
                c.draw_text(value[0]+value[2]/2, value[1]+value[3]/2, 
                            value[2]*.95,  key, fg="black")
            
            else: 
                c.draw_text_vertical(value[0]+value[2]/2, value[1]+value[3]/2, 
                                     value[3] *.85,  key, fg="black")

    ### START: DO NOT CHANGE THIS CODE ###
    # save or show the result.
    if output_filename:
        print("saving...", output_filename)
        c.savefig(output_filename)
    else:
        c.show()
    ### END: DO NOT CHANGE THIS CODE ###


               