import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def dodawanie():
    imie=input("Podaj imie: ")
    while True:
        try:
            wiek=int(input("Podaj wiek: "))
            if wiek<=0:
                print("Wiek musi byc liczba wieksza od zera!")
            else:
                break  
        except:
            print("Wiek musi byc liczba!")
        
    while True:
        try:
            nrbuta=int(input("Podaj numer buta: "))
            if nrbuta<=0:
                print("Numer buta musi byc liczba wieksza od zera!")
            else:
                break
        except:
            print("Numer buta musi byc liczba!")
       
    while True:
        try:
            wzrost=int(input("Podaj wzrost: "))
            if wzrost<=0:
                print("Wzrost musi byc liczba wieksza od zera!")
            else:
                break
        except:
            print("Wzrost musi byc liczba wieksza od zera!")
        
    tytul=input("Podaj tytul ulubionej ksiazki/filmu: ")  
    df.loc[len(df)] = {'imie': imie, 'wiek': wiek, 'numer buta': nrbuta, 'wzrost': wzrost, 'tytul ulubionej ksiazki/filmu': tytul}
    df.to_excel(r'plik.xlsx', index = False)
    print(df)

def usuwanie():
    a=int(input("Ktory wiersz chcesz skasowac?: "))
    a=a-1
    df=dataframe.drop(a)
    df.to_excel(r'plik.xlsx', index = False)
    print(df)

def sortowanie():
    b=input("Wedlug ktorego parametru chcesz dokonac sortowania? 1-imie 2-wzrost 3-wiek")
    if b=='1':
        df=dataframe.sort_values('imie')
    elif b=='2':
        df=dataframe.sort_values('wzrost')
    elif b=='3':
        df=dataframe.sort_values('wiek')
    df.to_excel(r'plik.xlsx', index = False)
    print(df)

def wyswietlanie():
    df = pd.read_excel('plik.xlsx')
    pd.set_option('display.max_rows', None)
    print(df)

def wykres():
    
    print("numer buta:", nrbuta,"wzrost:",wzrost)
    plt.xlabel("numer buta")
    plt.ylabel("wzrost")
    plt.scatter(nrbuta,wzrost)
    plt.show()

while True:
    df = pd.read_excel('plik.xlsx')
    df.columns = ['imie', 'wiek', 'numer buta', 'wzrost', 'tytul ulubionej ksiazki/filmu']
    imie=np.array(df['imie'])
    wiek=np.array(df['wiek'])
    nrbuta=np.array(df['numer buta'])
    wzrost=np.array(df['wzrost'])
    tytul=np.array(df['tytul ulubionej ksiazki/filmu'])
    dataframe = pd.DataFrame({"imie": imie, "wiek": wiek, "numer buta": nrbuta, "wzrost": wzrost, "tytul ulubionej ksiazki/filmu": tytul})
    x=input("Wybierz akcje. 1-dodaj nowy wpis, 2-skasuj wybrany wpis, 3-sortuj wedlug, 4-wyswietl zawartosc, 5-narysuj wykres, 6-zakoncz ")
    if x=='1':
        dodawanie()
    if x=='2':
        usuwanie()
    if x=='3':
        sortowanie()
    if x=='4':
        wyswietlanie()
    if x=='5':
        wykres()
    if x=="6":
        quit()


