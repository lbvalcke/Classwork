import json

cfpb_16 = [x for x in json.load(open("cfpb16_1000.json"))]

# Task 1
def count_complaints(complaints, company_name):
    # Your code goes here
    # replace 0 with a suitable return value
    company = 0
    
    for complaint in complaints: 
        if company_name == complaint["Company"]:
            company += 1

    return company


# Task 2
def find_companies(complaints):
    # Your code goes here
    # replace [] with a suitable return value
    company_list = set()
    
    for complaint in complaints:
        company_list.add(complaint["Company"])
    
    return company_list


# Task 3
def count_by_state(complaints):
    # Your code goes here
    # replace {} with a suitable return value
    by_state = {}
    
    for complaint in complaints:
        state = complaint["State"]
        if state not in by_state:
            by_state[state] = 0
        by_state[state] += 1
    
    return by_state


# Task 4
def count_by_company_by_state(complaints):
    # Your code goes here
    # replace {} with a suitable return value
    by_company_by_state = {}

    for complaint in complaints:
        
        company = complaint["Company"]
        state = complaint["State"]
        
        by_company_by_state[company] = by_company_by_state.get(company, {})
        by_company_by_state[company][state] = by_company_by_state[company].get(state, 0) + 1


    return by_company_by_state
        

# Task 5
def complaints_by_company(complaints):
    # Your code goes here
    # replace {} with a suitable return value
    complaints_by_company = {}

    for complaint in complaints:

        company = complaint["Company"]
        complaints_by_company[company] = complaints_by_company.get(company, [])
        complaints_by_company[company].append(complaint) 

    return complaints_by_company    
