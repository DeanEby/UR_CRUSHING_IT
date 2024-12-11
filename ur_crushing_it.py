# TODO take investment money and start calculating compounding interest over time.
# TODO same with savings, and after $5000 in bank we can shift the % to investments
# TODO take debt money and apply it to loans over time. 
# TODO see how wealth ((investments + savings) - debt) looks over time
# TODO do some automatic rebalancing of investment, debt payment, and other factors to find 
# optimal distribution
# TODO compare standard budget to real spending and see how they compare
# TODO read up on optimal standard budget
# DONE write file reading logic for importing data. Use .gitignore to make sure those files aren't added to repo

# initializing some global variables
savings_goal = 5000
snp500_estimated_performance = .08
# How many years do we simulate
PERIOD = 20

bank = 0
investment_portfolio = []
debt_portfolio = {}

# Reading in debt
# A csv file with name, balance, interest_rate as column names
debt_file = open("UR_CRUSHING_IT/secrets/debt.csv", "r")
column_names = debt_file.readline()

for line in debt_file:
    line = line.strip()
    line = line.split(",")
    debt_portfolio[line[0]] = [float(line[1]), float(line[2])]
print(debt_portfolio)



# Reading in salary value
# Just a text file with a number in it
monthly_salary_file = open("UR_CRUSHING_IT/secrets/monthly_salary.txt", "r")

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


budgeting_percentage_dict_values = list(standard_budgeting_percentage_dict.values())
budgeting_percentage_dict_keys = list(standard_budgeting_percentage_dict.keys())

def check_budget_percentage(expenses_dict):
    expenses_dict_values = list(expenses_dict.values())
    percentage_total = sum(expenses_dict_values)
    if percentage_total == 100:
        return True
    else:
        return False

def ask_for_monthly_net_income():
    loop = True
    while loop:
        net_income = input("Please enter your monthly net income as a whole number: ")
        if check_is_digit(net_income):
            loop = False
    return net_income


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

def calculate_dollars_from_percentage(monthly_salary, expenses_dict):
    expenses_dict_values = list(expenses_dict.values())
    expenses_dict_keys = list(expenses_dict.keys())
    expenses_dollars_dict = {}
    for expense in expenses_dict_keys:
        decimal = expenses_dict[expense] / 100
        dollar_amount = monthly_salary * decimal
        expenses_dollars_dict[expense] = dollar_amount
    return expenses_dollars_dict

def dict_to_string(dictionary):
    return str(dictionary).replace("{", "").replace("}", "").replace("'", "")
    

standard_monthly_dollar_budget = calculate_dollars_from_percentage(monthly_salary, standard_budgeting_percentage_dict)
smdb_string = dict_to_string(standard_monthly_dollar_budget)

print("Standard Budget for %s monthly salary is:" % monthly_salary, smdb_string)

        



