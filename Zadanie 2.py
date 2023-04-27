import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
while True:
    try:
        A=float(input("Podaj amplitudę oscylacji: "))
        if (A>0):
            break
        else:
            print("Wartości muszą być dodatnie! Wprowadź dane ponownie. ")
    except:
        print("Podana wartość jest nieprawidłowa!")
while True:
    try:
        a=float(input("Podaj amplitude szumu o rozkładzie jednorodnym: "))
        if (a > 0):
            break
        else:
            print("Wartości muszą być dodatnie! Wprowadź dane ponownie. ")
    except:
        print("Podana wartość jest nieprawidłowa!")
while True:
    try:
        f=float(input("Podaj częstotliwość oscylacji: "))
        if (a > 0):
            break
        else:
            print("Wartości muszą być dodatnie! Wprowadź dane ponownie. ")
    except:
        print("Podana wartość jest nieprawidłowa!")
while True:
    try:
        koniec=int(input("Podaj koniec wektora: "))
        if (a > 0):
            break
        else:
            print("Wartości muszą być dodatnie! Wprowadź dane ponownie. ")
    except:
        print("Podana wartość jest nieprawidłowa!")
while True:
    try:
        krok=int(input("Podaj liczbe punktów: "))
        if (a > 0):
            break
        else:
            print("Wartości muszą być dodatnie! Wprowadź dane ponownie. ")
    except:
        print("Podana wartość jest nieprawidłowa!")
while True:
    try:
        gamma=float(input("Podaj współczynnik tłumienia: "))
        if (A>0) and (a>0) and (f>0) and (koniec>0) and (krok>0) and (gamma>0):
            break
        else:
            print("Wartości muszą być dodatnie! Wprowadź dane ponownie. ")
    except:
        print("Podana wartość jest nieprawidłowa!")
t=np.linspace(0, koniec, krok)
aNt=a*(np.random.rand(len(t))-0.5)
y= A*np.sin(2*np.pi*f*t)*np.e**(-gamma*t)+aNt
plt.plot(t,y)
plt.xlabel('t')
plt.ylabel('f(t)')
plt.title('y=a*sin(2*pi*f*t)*e**(-gamma*t)+aNt')
plt.show()
z=input("Czy zapisać do pliku? t-tak, n-nie ")
if z=="t":
    nazwa = input("Jak nazwać plik? ")
    data = {"t":t,"y":y} #tworzy słownik klucz-wartość przechowujący dane
    dataframe = pd.DataFrame(data) #tworzy pandas dataframe+
    dataframe.to_csv(nazwa, index=False, sep="\t")

z=input("Czy chcesz dokonać dopasowania parametrów? t-tak, n-nie ")
if z=="t":
    dataframe = pd.DataFrame({"t": t, "y": y})
    print(dataframe)

def sinusoida(t,A,gamma,f):
    s= A*np.sin(2*np.pi*f*t)*np.e**(-gamma*t)
    return s

p0=[A, gamma, f] #wektor inicjalizujący
fit_params, covariance_matrix = curve_fit(sinusoida, t, y,p0=p0)
print("Parametry fitowania: \na = ", fit_params[0], '\nb = ', fit_params[1],'\nc = ', fit_params[2])
plt.scatter(t,y)
plt.title('y=a*sin(2*pi*f   *t)*e**(-gamma*t)')
plt.xlabel("time s")
plt.ylabel("f(t)")
plt.plot(t,y)
plt.plot(t, sinusoida(t, *fit_params), 'r')
plt.show()
