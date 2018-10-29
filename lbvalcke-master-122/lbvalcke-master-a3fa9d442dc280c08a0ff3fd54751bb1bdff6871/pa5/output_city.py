# CS121 Linear regression assignment
# 
<<<<<<< HEAD
# Luis Buenaventura 438594
#
# Print text answers for the CITY data
#
import sys
import model  
=======
# YOUR NAME
#
# Print text answers for the CITY data
#
>>>>>>> 773dcd3fdb9e1695ebc8bfcf1f2696415922ed23

# useful defined constants for the city data
PREDICTOR_VAR_INDICES = list(range(0, 7))
DEPENDENT_VAR_INDEX = 7	

<<<<<<< HEAD
# names operation
data_name = "CITY"

# loads data
labels, pre_dataset, result_dataset = model.data_selector("data/city/training.csv", PREDICTOR_VAR_INDICES, DEPENDENT_VAR_INDEX)
t_labels, test_pre_dataset, test_result_dataset = model.data_selector("data/city/testing.csv", PREDICTOR_VAR_INDICES, DEPENDENT_VAR_INDEX)

# calls result for task 1
model.format_task1(data_name, labels, pre_dataset, result_dataset)

# calls result for task 2
model.format_task2(data_name, labels, pre_dataset, result_dataset)

# calls result for task 3
model.format_task3(data_name, DEPENDENT_VAR_INDEX, 0.1, 0.01, labels, pre_dataset, result_dataset)

# calls result for task 4
model.format_task4(data_name, DEPENDENT_VAR_INDEX, pre_dataset, result_dataset, test_pre_dataset, test_result_dataset, labels)

=======
>>>>>>> 773dcd3fdb9e1695ebc8bfcf1f2696415922ed23
if __name__ == "__main__":
    # remove the next line
    pass
