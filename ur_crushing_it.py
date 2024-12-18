# TODO take investment money and start calculating compounding interest over time.
# TODO same with savings, and after $5000 in bank we can shift the % to investments
# TODO take debt money and apply it to loans over time. 
# TODO see how wealth ((investments + savings) - debt) looks over time
# TODO do some automatic rebalancing of investment, debt payment, and other factors to find 
# optimal distribution
# TODO compare standard budget to real spending and see how they compare
# TODO read up on optimal standard budget

import pandas as pd


# initializing some global variables
savings_goal = 5000
snp500_estimated_performance = .08
# How many years do we simulate
PERIOD = 6
# how much +- are % are we introducing to find optimal budget
WIGGLE = 0
#current_year = 0

bank = open("secrets/bank.txt")
investment_portfolio = []
#debt_portfolio = {}

debt_df = pd.read_csv("secrets/debt.csv")
debt_df['monthly_interest_rate'] = debt_df.apply(lambda row: row.interest_rate / 12, axis = 1)
#print(debt_df)

# Reading in salary value
# Just a text file with a number in it
monthly_salary_file = open("secrets/monthly_salary.txt", "r")

monthly_salary = float(monthly_salary_file.readline())
monthly_salary_file.close()
#print(monthly_salary)

def check_is_digit(input_str):
    if input_str.strip().isdigit():
        return True
    else:
        return False


standard_budgeting_percentage_dict = {"housing": 30, # need
                            "savings": 5,# saving
                            "food": 10, # need
                            "investments": 10, # savings
                            "transportation": 5, # need
                            "insurance": 10, # need
                            "debt": 10, # savings
                            "entertainment": 10, # want
                            "personal": 10} # want

# for now we only need to know debt % and investments %
real_budgeting_percentage_dict = {"debt": 10,
                                  "investments": 10}



budgeting_percentage_dict_values = list(standard_budgeting_percentage_dict.values())
budgeting_percentage_dict_keys = list(standard_budgeting_percentage_dict.keys())


# Checks to make sure the sum of the budget percentages does not 
# surpass 100
def check_budget_percentage(expenses_dict):
    expenses_dict_values = list(expenses_dict.values())
    percentage_total = sum(expenses_dict_values)
    if percentage_total == 100:
        return True
    else:
        return False

# asks the user for their monthly net income

def ask_for_monthly_net_income():
    loop = True
    while loop:
        net_income = input("Please enter your monthly net income as a whole number: ")
        if check_is_digit(net_income):
            loop = False
    return net_income

# asks the user for their monthly expenses
# TODO create calculate_percentage_from_dollars() function
# will need this for this function to be compatible
# with the rest of the program
def ask_for_monthly_expenses(expenses):
    # expenses is a list of expense catagories ex: ["savings", "housing", "food"]
    monthly_expenses = {}
    for category in expenses:
        loop = True
        while loop:
            tempval = input("Please enter your monthly %s payment as a whole number: " % category)
            if check_is_digit(tempval):
                loop = False
        monthly_expenses[category] = tempval
    return monthly_expenses

# takes a budget expressed as percentages as well as a monthly salary, and uses
# that information to create a budget expressed as dollars spent
def calculate_dollars_from_percentage(monthly_salary, expenses_dict):
    expenses_dict_values = list(expenses_dict.values())
    expenses_dict_keys = list(expenses_dict.keys())
    expenses_dollars_dict = {}
    for expense in expenses_dict_keys:
        decimal = expenses_dict[expense] / 100
        dollar_amount = monthly_salary * decimal
        expenses_dollars_dict[expense] = dollar_amount
    return expenses_dollars_dict

# string representation of a dictionary
def dict_to_string(dictionary):
    return str(dictionary).replace("{", "").replace("}", "").replace("'", "")
    

standard_monthly_dollar_budget = calculate_dollars_from_percentage(monthly_salary, standard_budgeting_percentage_dict)
smdb_string = dict_to_string(standard_monthly_dollar_budget)

#print("Standard Budget for %s monthly salary is:" % monthly_salary, smdb_string)


    # Current algorithm does not account for minimum required payments
def calculate_debt_after_period(period, debt_df, expenses_dict):
    # convert budget % to dollars
    dollar_dict = calculate_dollars_from_percentage(monthly_salary, expenses_dict)
    # how many loans are in our debt_df
    loan_count = len(debt_df)
    # get the amount of money budgeted for paying off debt
    debt_monthly_budgeted = dollar_dict["debt"]

    
    for year in range(period):



        # each month we make a payment
        for month in range(12):
            loan_interest_dict = {}
            # accessing each loan in debt df
            for row in range(loan_count):
                # checking for paid off loans
                # TODO remove paid off loans
                if debt_df.iloc[row]["balance"] <= 0:
                    # currently if a loan is paid off we return so we can look at prints
                    return 
                
                # rounding here may add up significantly over time, may need to make changes
                # for each loan, calculate the interest owed
                interest = float(debt_df.iloc[row]["balance"] * debt_df.iloc[row]["monthly_interest_rate"])
                # add the owed interest to a dictionary
                loan_interest_dict[debt_df.iloc[row]["name"]] = interest
                debt_df['monthly_interest_rate'] = debt_df.apply(lambda row: row.interest_rate / 12, axis = 1)
            
            # Calculate which loans are generating the most interest
            loan_interest_total = sum(loan_interest_dict.values())
            loan_interest_percent = {}
            # calculate the relative percentages of the loans
            for loan in loan_interest_dict:
                #print(loan_interest_dict[loan])
                loan_interest_percent[loan] = ( loan_interest_dict[loan] / loan_interest_total)
            #print(sum(loan_interest_percent.values()))
            
            
            

            # Simulate paying off the loan
            for loan in loan_interest_dict:
                df_row = debt_df.loc[debt_df['name'] == loan]
                index = debt_df.loc[debt_df['name'] == loan].index[0]
                balance = df_row['balance']
                balance = float(balance.iloc[0])
                
                payment = debt_monthly_budgeted * loan_interest_percent[loan]

                debt_balance = (balance + loan_interest_dict[loan]) - payment
                debt_df.iloc[index, 1] = debt_balance
                
                #print(payment)
            print("Month:", month)
            print("Year:", year)
            print("Most impactful loan to pay off:", max(loan_interest_percent, key=loan_interest_percent.get))
            print("Amount of money from interest by loan", dict_to_string(loan_interest_dict))
            print(debt_df)
            



    return # need to design an output for this

def pay_debt(debt_df, amount):
    # dictionary to store the amount of interest being generated
    loan_interest_dict = {}
    
    # the amount of money allocated to pay off debt
    debt_monthly_budgeted = amount

    # how many loans are in our debt_df
    loan_count = len(debt_df)

    # how many active loans are in debt_df
    active_loan_count = 0

    # checking for paid off loans
    for row in range(loan_count):
        if debt_df.iloc[row]["balance"] <= 0:
            debt_df.iloc[row, 1] = 0
        else:
            active_loan_count += 1
            #return 

    # for each loan add the interest to the loan
    for row in range(loan_count):    
        # for each loan, calculate the interest owed in dollars
        interest = float(debt_df.iloc[row]["balance"] * debt_df.iloc[row]["monthly_interest_rate"])
        
        #print("interest:", interest)
        # add the owed interest to the dictionary
        loan_interest_dict[debt_df.iloc[row]["name"]] = interest
    #return
    # Calculate which loans are generating the most interest
    loan_interest_total = sum(loan_interest_dict.values())
    loan_interest_percent_dict = {}
    # calculate the relative percentages of the loans
    for loan in loan_interest_dict:
        loan_interest_percent_dict[loan] = ( loan_interest_dict[loan] / loan_interest_total)


    print("should be 100:",sum(loan_interest_percent_dict.values()))
    # Simulate paying off the loan
    extra = 0
    total_debt = debt_df['balance'].sum()
    extra = debt_monthly_budgeted - total_debt
    

    for loan in loan_interest_dict:
        # find the row in the dataframe that matches the current loan
        
        df_row = debt_df.loc[debt_df['name'] == loan]
        
        index = debt_df.loc[debt_df['name'] == loan].index[0]
        balance = df_row['balance']
        balance = float(balance.iloc[0])
        if extra > 0:
            print("sum of debt", sum(loan_interest_dict.values()))
            print(total_debt)
            # print("wtf")
            payment = total_debt * loan_interest_percent_dict[loan]
        else:
            payment = debt_monthly_budgeted * loan_interest_percent_dict[loan]

        # print("debt amount:", debt_df.iloc[index, 1])
        # print("amount paid:", payment)
        
        debt_balance = (balance + loan_interest_dict[loan]) - payment
        debt_df.iloc[index, 1] = debt_balance
    return debt_df, extra
#debt_calculation = calculate_debt_after_period(PERIOD, debt_df, standard_budgeting_percentage_dict)








for i in range(WIGGLE + 1):
# TODO handle different budget configurations    

    # main loop
    for year in range(PERIOD):
        # I don't like having the year start at 0
        year = year + 1

        for month in range(12):
            # I don't like having the month start at 0
            month = month + 1
            this_months_salary = monthly_salary
            this_months_budget = calculate_dollars_from_percentage(this_months_salary, real_budgeting_percentage_dict)
            debt_budget = this_months_budget["debt"]
            investments_budget = this_months_budget["investments"]
            debt_df, extra_funds = pay_debt(debt_df, 500)
            #print(debt_df)

            print("year", year, "month", month, "\n", debt_df)

            #print(this_months_budget)
            #print(month)
            #print(standard_monthly_dollar_budget)