# Import the libraries needed
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Function to get a valid input from the user
def get_valid_number(prompt_text, allow_zero=False):
    while True:
        text = input(prompt_text)
        try:
            number = float(text)
        except ValueError:
            print("Please enter a valid number, try again.")
            continue
        
        if allow_zero:
            if number < 0:
                print("Please enter a non-negative number, try again.")
                continue
        else:
            if number <= 0:
                print("Please enter a positive number, try again.")
                continue
            
        return number

# Define variables for the mortgage calculation
principal = get_valid_number("Loan Principal (PLN): ")
years = get_valid_number("Term(Years): ", allow_zero=False)
annual_interest_rate = get_valid_number("Interest Rate (%): ")
overpayment = get_valid_number("Monthly Overpayment (PLN): ", allow_zero=True)

# A fixed-rate mortgage payment is calculated with this formula:
# M = P[r(1+r)^n]/[(1+r)^n-1]
# Where:
# M = fixed monthly payment
# P = principal loan amount
# r = monthly interest rate (annual interest rate divided by 12)
# n = number of payments (loan term in months)

# Convert input to percentage and to monthly
monthly_interest_rate = annual_interest_rate / 100 / 12
# Convert years to months for the number of payments
number_of_payments = years * 12
# Calculate the fixed monthly payment using the formula
monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)

# For sanity check
base_line_case = monthly_payment * number_of_payments - principal

# Define a function to simulate the mortgage payments and calculate the total interest paid and months elapsed
def simulate_mortgage(principal, monthly_interest_rate, monthly_payment, overpayment):
    balance = principal
    total_interest_paid = 0
    months_elapsed = 0
    # Loop until the balance is paid off
    while balance > 0.01: #0.01 is due to floating point precision issues
        # Calculate this month's interest
        interest_this_month = balance * monthly_interest_rate
        # Add the interest to the total interest paid
        total_interest_paid += interest_this_month
        # Calculate how much of the payment acutally reduces the balance
        principal_repayment = monthly_payment + overpayment - interest_this_month
        # balance is reduced
        balance -= principal_repayment
        # Increment the number of months elapsed
        months_elapsed += 1
        # safety guard
        if months_elapsed > 1000:
            print("Error")
            break
        
    return months_elapsed, total_interest_paid

# Simulate the mortgage for both the baseline and overpayment scenarios
base_months, base_interest = simulate_mortgage(principal, monthly_interest_rate, monthly_payment, 0)
scenario_months, scenario_interest = simulate_mortgage(principal, monthly_interest_rate, monthly_payment, overpayment)

# Calculate the years and interest saved by making overpayments
years_saved = (base_months - scenario_months) / 12
interest_saved = base_interest - scenario_interest

print(f"Years Saved: {years_saved:.2f} years")
print(f"Interest Saved: {interest_saved:,.2f} PLN")

# Calculate the total amount paid in both scenarios
total_baseline = principal + base_interest
total_scenario = principal + scenario_interest

print(f"Total Paid in Baseline Scenario: {total_baseline:,.2f} PLN")
print(f"Total Paid in Overpayment Scenario: {total_scenario:,.2f} PLN")

# Plotting the results
category_labels = ['Baseline', 'Scenario']
principal_segment = [principal, principal]
interest_segment = [base_interest, scenario_interest]

# Define a function to format the x-axis labels in thousands (K) and millions (M)
def axis_formatter(value, position):
    if value < 1000000:
        return f'{int(value/1000)}K'
    else:
        return f'{value/1000000:.1f}M'

# Create a horizontal bar chart to visualize the total cost of the mortgage in both scenarios
plt.barh(category_labels, principal_segment, label = 'Principal', color = 'blue')
plt.barh(category_labels, interest_segment, left = principal_segment, label = 'Interest', color = 'green')
# Add a vertical dashed line to indicate the total cost of the overpayment scenario
plt.axvline(x=total_scenario, linestyle='--', color='gray')
# Set the x-axis formatter to use the defined axis_formatter function
plt.gca().xaxis.set_major_formatter(FuncFormatter(axis_formatter))
# Add legend, labels, title, and additional information about time and interest saved
plt.legend()
plt.xlabel('Total Cost (PLN)')
plt.title('Mortgage Calculator')
# Invert the y-axis to have the baseline scenario on top
plt.gca().invert_yaxis()
# Add text to the bottom of the plot to show the time and interest saved
plt.figtext(0.3, 0.02, f"TIME SAVED (YEARS)\n{years_saved:.1f}", ha='center', fontsize=12)
plt.figtext(0.7, 0.02, f"INTEREST SAVED (PLN)\n{interest_saved:,.0f}", ha='center', fontsize=12)
plt.subplots_adjust(bottom=0.25)
# Show the plot
plt.show()