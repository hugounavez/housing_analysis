import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from MorgateCalculator import *

def mortgage_payments(loan_amount, interest_rate, years):
    # Convert interest rate to decimal
    interest_rate = interest_rate / 100
    
    # Convert years to months
    months = years * 12
    
    # Calculate monthly interest rate
    monthly_interest_rate = interest_rate / 12
    
    # Calculate monthly payment
    monthly_payment = loan_amount * (monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** (-months)))
    
    # Initialize lists
    payments_to_principal = []
    payments_to_interest = []
    total_payments = []
    
    # Initialize remaining loan amount
    remaining_loan_amount = loan_amount
    
    # Loop through each month
    for month in range(1, months + 1):
        # Calculate payment to principal
        payment_to_principal = monthly_payment - (remaining_loan_amount * monthly_interest_rate)
        
        # Calculate payment to interest
        payment_to_interest = monthly_payment - payment_to_principal
        
        # Calculate remaining loan amount
        remaining_loan_amount = remaining_loan_amount - payment_to_principal
        
        # Append to lists
        payments_to_principal.append(payment_to_principal)
        payments_to_interest.append(payment_to_interest)
        total_payments.append(monthly_payment)
        
    return payments_to_principal, payments_to_interest, total_payments




# Calculating maintenance costs of a house
# https://www.homekeep.com/learning-center/the-truth-about-the-annual-cost-of-home-maintenance/#:~:text=This%20means%20the%20average%20homeowner,a%20number%20of%20other%20factors.

# Function to return a list of payment per months that represents 1 percent of a home's value per year, given the home value, appreciation rate, and number of years
def monthy_maintenance_cost(property_value, appreciation_rate, years):
    monthy_maintenance_cost_all_months = []
    for i in range(1, years + 1):
        property_value = property_value * (1 + appreciation_rate / 100)
        # rule of thumb: 1% of property value per year
        maintenance_per_year = property_value * (1 / 100)
        monthly_property_tax = [maintenance_per_year / 12] * 12
        monthy_maintenance_cost_all_months.append(monthly_property_tax)
    
    # return monthy_maintenance_cost_all_months flatened
    return [item for sublist in monthy_maintenance_cost_all_months for item in sublist]


#Home Appreciation
#https://www.creditkarma.com/home-loans/i/average-home-value-increase-per-year

# Function to return the property tax monthly payments given the property value, the appreciation rate and the property tax rate, years
def property_tax(property_value, appreciation_rate, property_tax_rate, years):

    monthly_property_tax_all_payments = []
    for i in range(1, years + 1):
        property_value = property_value * (1 + appreciation_rate / 100)
        property_tax = property_value * (property_tax_rate / 100)
        monthly_property_tax = [property_tax / 12] * 12
        monthly_property_tax_all_payments.append(monthly_property_tax)

    # return a flap list of monthly property tax payments
    return [item for sublist in monthly_property_tax_all_payments for item in sublist]


# function that returns the closing costs of a loan given the loan amount and the closing cost rate
def calculate_closing_costs(loan_amount, closing_cost_rate=4.5):
    return loan_amount * (closing_cost_rate / 100)

# function that returns the rent monthly payments given the rent per month, the inflation rent rate and the number of years
# note: first year rent is the rent given
def rent_payments(rent_per_month, inflation_rent_rate, years):
    monthly_rent_payments = [rent_per_month] * 12
    for i in range(2, years + 1):
        rent_per_month = rent_per_month * (1 + inflation_rent_rate / 100)
        total_rent_months = [rent_per_month] * 12
        for month in total_rent_months:
            monthly_rent_payments.append(month)

    # return a flat list of monthly rent payments
    return monthly_rent_payments




def home_insurance_pay_per_month(property_value):
    home_issurance = 1953 # per year
    average_home_nj = 420000
    return (property_value * (home_issurance / average_home_nj)) / 12.0

# Function to return home insurance payments given the property value, appreciation rate, and number of years
def home_insurance(property_value, appreciation_rate, years):
    home_insurance_all_payments = []
    for i in range(1, years + 1):
        property_value = property_value * (1 + appreciation_rate / 100)
        home_insurance = home_insurance_pay_per_month(property_value)
        monthly_home_insurance = [home_insurance] * 12
        home_insurance_all_payments.append(monthly_home_insurance)

    # return a flap list of monthly home insurance payments
    return [item for sublist in home_insurance_all_payments for item in sublist]

# create a function that given the number of years, it will return a list of dates of first day of each month of every year
# Note: each date is the first day of the month, for example, if years=30, then lenth of the result list would be 30x12=360

def get_dates(years):
    dates = []
    current_date = datetime.today()
    for i in range(1, years + 1):
        for month in range(1, 13):
            current_date = current_date + relativedelta(months=+1)
            dates.append(current_date)
    return dates



# create a function that given a list of equity per month, and down payment, and closing costs, it will return the index in which the equity is greater than the down payment plus the closing costs
def get_index_equity_greater_than_down_payment(equity, down_payment, closing_costs):
    for i in range(0, len(equity)):
        if equity[i] > (down_payment + closing_costs):
            return i
    return -1



def evaluate_home(zillow_home_price, appreciation_rate, property_tax_rate, closing_cost_rate, down_payment_percent, interest_rate, rent_per_month, rent_inflation_rate, years):

    loan_amount = zillow_home_price * (1 - down_payment_percent / 100)

    monthly_total_principal,monthly_total_interests, monthly_total_payments = mortgage_payments(loan_amount, interest_rate, years)
    monthly_maintenance_cost = monthy_maintenance_cost(zillow_home_price, appreciation_rate, years)
    monthly_property_tax = property_tax(zillow_home_price, appreciation_rate, property_tax_rate, years)
    monthly_home_insurance = home_insurance(zillow_home_price, appreciation_rate, years)
    closing_costs = calculate_closing_costs(loan_amount, closing_cost_rate)

    # calculate total monthly payment with all costs index wise
    total_monthly_payments = []
    for i in range(0, len(monthly_maintenance_cost)):
        total_monthly_payments.append(monthly_total_payments[i] + monthly_maintenance_cost[i] + monthly_property_tax[i] + monthly_home_insurance[i])


    df = pd.DataFrame({'total_monthly_payments': total_monthly_payments, 'monthly_total_principal': monthly_total_principal, 'monthly_total_interests': monthly_total_interests, 'monthly_total_payments': monthly_total_payments, 'monthly_maintenance_cost': monthly_maintenance_cost, 'monthly_property_tax': monthly_property_tax, 'monthly_home_insurance': monthly_home_insurance})

    # add a new column with the equity of the house including and the monthly payment to principal, and the down payment
    df['equity'] = df['monthly_total_principal'].cumsum() + (zillow_home_price * (down_payment_percent / 100))

    # add a new column with the acumulated total_monthly_payments and the down payment and the closing_costs    
    df['accumulated_costs'] = (df['total_monthly_payments'].cumsum() + (zillow_home_price * (down_payment_percent / 100)) + closing_costs).round(2)
    #df['accumulated_costs'] = df['accumulated_costs'].round(2)

    # Add a hypothetical rent per month column to compare the rent vs buy
    df['rent_per_month'] = rent_payments(rent_per_month, rent_inflation_rate, years) 

    df['accumulated_rent'] = df['rent_per_month'].cumsum().round(2)

    df['proyected_home_appreciation'] = rent_payments(zillow_home_price, appreciation_rate, 30)

    df['dates'] = get_dates(30)

    return df


def plot_costs_equity(df, home_price,down_payment_percent,  closing_cost_rate):
        
    plt.plot(df["dates"], df['accumulated_costs'], label='Costs')
    plt.plot(df["dates"], df['accumulated_rent'], label='Rent')
    plt.plot(df["dates"], df['equity'], label='Equity')
    plt.plot(df["dates"], df['proyected_home_appreciation'], label='Home Appreciation')
    # plot a line represeting closing_costs + down_payment
    loan_amount = home_price * (1 - down_payment_percent / 100)
    closing_costs = calculate_closing_costs(loan_amount, closing_cost_rate)
    plt.axhline(y=closing_costs + (home_price * (down_payment_percent / 100)), color='r', linestyle='--', label='Down Payment + Closing Costs')
    plt.xlabel('Years')
    plt.ylabel('Accumulated Costs')
    plt.title('Rent vs Buy')
    # grid on
    plt.grid(True)
    # set y axis in dollars
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))
    plt.legend()

    plt.show()