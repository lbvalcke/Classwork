# CS121 Linear regression assignment
# 
<<<<<<< HEAD
# Luis Buenaventura 438594
=======
# YOUR NAME and CNET ID HERE
>>>>>>> 773dcd3fdb9e1695ebc8bfcf1f2696415922ed23
#
# Print text answers for the STOCK data
#
import sys
<<<<<<< HEAD
import model
=======
>>>>>>> 773dcd3fdb9e1695ebc8bfcf1f2696415922ed23

# useful defined constants for the stock data
PREDICTOR_VAR_INDICES = list(range(0, 11))
DEPENDENT_VAR_INDEX = 11

<<<<<<< HEAD
# defines name of operation
data_name = "STOCK"

# loads data
labels, pre_dataset, result_dataset = model.data_selector("data/stock/training.csv", PREDICTOR_VAR_INDICES, DEPENDENT_VAR_INDEX)
t_labels, test_pre_dataset, test_result_dataset = model.data_selector("data/stock/testing.csv", PREDICTOR_VAR_INDICES, DEPENDENT_VAR_INDEX)

# calls task 1 result
model.format_task1(data_name, labels, pre_dataset, result_dataset)

# calls task 2 result
model.format_task2(data_name, labels, pre_dataset, result_dataset)

# calls task 3 result
model.format_task3(data_name, DEPENDENT_VAR_INDEX, 0.1, 0.01, labels, pre_dataset, result_dataset)

# calls task 4 result
model.format_task4(data_name, DEPENDENT_VAR_INDEX, pre_dataset, result_dataset, test_pre_dataset, test_result_dataset, labels)


=======
>>>>>>> 773dcd3fdb9e1695ebc8bfcf1f2696415922ed23
if __name__ == "__main__":
    # remove the next line
    pass
