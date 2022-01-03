#Taking inputs from the user to calculate the time taken to pay downpayment
annual_salary = float(input('Enter your annual salary: '))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost = float(input('Enter the total cost of your dream home: '))
semi_annual_raise = float(input('Enter the semi-annual raise, as a decimal: '))

#Rate of interest on current savings invested
r = 0.04100

#Percentage of amount to be paid as down payment for house (in decimal)
portion_down_payment = 0.25 
down_payment = portion_down_payment*total_cost


#Calculationg monthly savings
mon_salary = annual_salary/12
mon_inv_return = r/12

#Taking initial savings as $0 and time as 0 months
total_months = 0
savings = 0


#looping in an while loop to only exist when the current savings is greater than or equal to down_payment

while savings < down_payment:
    savings += portion_saved*mon_salary + savings*mon_inv_return
    if total_months%6 == 0 and total_months != 0:       ###################Condition to check if the month is Semi year or not. The increased salary be will issued next month. Hence salary increase after the savings.
        mon_salary *= (1+semi_annual_raise)
    total_months += 1

#Printing the final output
print("Number of months: %s" %total_months)