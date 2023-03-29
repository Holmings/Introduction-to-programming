import tkinter as tk
import requests


class CurrencyConverter:
    def __init__(self):
        self.base_url = "http://api.nbp.pl/api/exchangerates/rates/a/"
        self.currency = "usd"
        self.rows = 10

    def get_currency_data(self):
        url = self.base_url + self.currency + "/last/" + str(self.rows) + "?format=json"
        response = requests.get(url)
        return response.json()['rates']


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Currency Converter")
        self.geometry("500x500")

        self.currency_converter = CurrencyConverter()

        self.currency_label = tk.Label(self, text="Currency:")
        self.currency_label.grid(row=0, column=0)

        self.currency_button_usd = tk.Button(self, text="USD", command=lambda: self.change_currency("usd"))
        self.currency_button_usd.grid(row=1, column=0)

        self.currency_button_eur = tk.Button(self, text="EUR", command=lambda: self.change_currency("eur"))
        self.currency_button_eur.grid(row=1, column=1)

        self.currency_button_gbp = tk.Button(self, text="GBP", command=lambda: self.change_currency("gbp"))
        self.currency_button_gbp.grid(row=1, column=2)

        self.currency_button_gbp = tk.Button(self, text="CZK", command=lambda: self.change_currency("czk"))
        self.currency_button_gbp.grid(row=1, column=3)

        self.currency_button_gbp = tk.Button(self, text="CHF", command=lambda: self.change_currency("chf"))
        self.currency_button_gbp.grid(row=1, column=4)

        self.rows_label = tk.Label(self, text="Rows:")
        self.rows_label.grid(row=2, column=0)

        self.rows_button_10 = tk.Button(self, text="10", command=lambda: self.change_rows(10))
        self.rows_button_10.grid(row=3, column=0)

        self.rows_button_20 = tk.Button(self, text="20", command=lambda: self.change_rows(20))
        self.rows_button_20.grid(row=3, column=1)

        self.rows_button_30 = tk.Button(self, text="30", command=lambda: self.change_rows(30))
        self.rows_button_30.grid(row=3, column=2)

        self.data_text = tk.Text(self)
        self.data_text.grid(row=4, column=0, columnspan=8)

        self.get_currency_data()

    def change_currency(self, currency):
        self.currency_converter.currency = currency
        self.get_currency_data()

    def change_rows(self, rows):
        self.currency_converter.rows = rows
        self.get_currency_data()

    def get_currency_data(self):
        currency_data = self.currency_converter.get_currency_data() #lista słowników zwrócona z serwera api

        self.data_text.delete("1.0", tk.END)  #usunięcie zawartości pola tekstowego od 1 wiersza do samego końca aby móc wpisać nowe dane

        for data in currency_data: #iteracja po liście słowników
            date = data['effectiveDate']
            rate = data['mid']

            self.data_text.insert(tk.END, f"{date} - {rate}\n") #dodanie do pola tekstowego


if __name__ == "__main__":
    app = App()
    app.mainloop()