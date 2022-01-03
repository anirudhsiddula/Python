#Taking inputs annual_salary from the user
annual_salary = float(input('Enter your annual salary: '))

#Rate of interest on current savings invested
r = 0.04

#Percentage of amount to be paid as down payment for house (in decimal)
portion_down_payment = 0.25
total_cost = 1000000
semi_annual_raise = 0.07
down_payment = portion_down_payment*total_cost

#Calculationg monthly savings
mon_salary = annual_salary/12
temp = mon_salary

#monthly investment returns
mon_inv_return = r/12

#Setting few parameters with constants
savings = 0
bisection = 0
max = 1
min = 0
save_ratio = 1/2000

if(mon_salary*36<down_payment):
    #Condition to check if it is possible to save for down payment with 100% savings
    print('It is not possible to pay the down payment in three years')
else:
    while(True):
        #Calculating savings with "save_ratio"  on 36months duration
        for i in range(36):
            savings += (save_ratio*mon_salary)+(savings*mon_inv_return)
            if i%6 == 0 and i!=0:
                mon_salary += mon_salary*semi_annual_raise
        
        #Checking if the savings are within +-100 amount of down_payment
        if savings >= down_payment-100 and savings <= down_payment+100 :
            break
        
        #Condition to check savings is more than down_payment+margin. If yes, we reduce our save ratio divided by 2.
        elif savings >= down_payment+100 :
            max = save_ratio
            #decreasing save ratio divided by 2
            save_ratio = max/2.0
            #increasing bisection count
            bisection += 1
            #Reseting savings and Salary
            savings = 0
            mon_salary = temp
        
        #Condition to check savings is less than down_payment+margin. If No, we take average of min and max.
        else:
            min = save_ratio
            #taking average min and max
            save_ratio = (min+max)/2.0
            #increasing the bisection count
            bisection += 1
            #Reseting Savings and Salary
            savings = 0
            mon_salary = temp
    print('Best savings rate: ', round(save_ratio,4))
    print('Steps in bisection search: ', bisection)

