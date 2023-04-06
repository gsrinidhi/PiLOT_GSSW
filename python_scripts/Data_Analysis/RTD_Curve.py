import numpy as np
import pandas as pd
import sys

#Argument 1(Optional): Order of polynomial
#Argument 2(Optional): Lower temperature value
#Argument 3(Optional): Higher temperature value
#Default Option: n = 7, lvalue = -15, hvalue = 50
# To run: python .\RTD_Curve.py
# Enter resistance till you want to exit. To exit, press spacebar and enter
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
    
def fit_test(x,y,n):
    mymodel = np.poly1d(np.polyfit(x, y, n))
    return mymodel

def range_fit(x,y,n,start,stop):
    f = fit_test(x[start:stop],y[start:stop],n)
    return f

if len(sys.argv) == 1:
    lvalue = 15
    hvalue = 150
    n = 7

elif len(sys.argv) == 2:
    lvalue = 26
    hvalue = 91
    n = int(sys.argv[1])

elif len(sys.argv) == 4:
    n = int(sys.argv[1])
    lvalue = int(sys.argv[2]) + 40
    hvalue = int(sys.argv[3]) + 40

df = pd.read_excel("thermistor_calib.xlsx",header=None)
print(len(sys.argv))
voltage = list(df[2])#voltage
resistance_ideal = list(np.log10(df[1]))#ideal resistance
temperature = list(df[0])#temperature
print("Order = " + str(n))
print("lvalue = " + str(temperature[lvalue]))
print("rvalue = " + str(temperature[hvalue]))
fit = range_fit(voltage,temperature,n,lvalue,hvalue)

alpha = 3.248 / 4096
print("Voltage co-efficients are: ")
for i in range(n+1):
    print(fit.coefficients[i] * (alpha ** (7-i)))

while 1:
    k = (input("Enter resistance: "))
    if isfloat(k) == True:
        k = float(k)
        print("Resistance = " + str(k))
        #out = coeff[0] * k ** 7 + coeff[1] * k ** 6 + coeff[2] * k ** 5 + coeff[3] * k ** 4 + coeff[4] * k ** 3 + coeff[5] * k ** 2 + coeff[6] * k ** 1 + coeff[7]
        out = fit(np.log10(k))
        print("Temperature = " + str(out))
    else:
        break
else:
    print("Hello")
