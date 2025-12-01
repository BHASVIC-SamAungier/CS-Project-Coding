from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QStackedWidget)
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QTextDocument

import sys
import json
import matplotlib.pyplot as plt
import requests

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Investment Portfolio Tracker")

        #nav bar
        self.navbar = QHBoxLayout()
        self.home_button = QPushButton("Home")
        self.add_button = QPushButton("Add Investment")
        self.overview_button = QPushButton("Portfolio Overview")
        self.navbar.addWidget(self.home_button)
        self.navbar.addWidget(self.add_button)
        self.navbar.addWidget(self.overview_button)

        #stacked pages
        self.stacked = QStackedWidget()
        self.home_page = self.create_home_page()
        self.add_page = self.create_add_investment_page()
        self.overview_page = self.create_portfolio_overview_page()
        self.stacked.addWidget(self.home_page)
        self.stacked.addWidget(self.add_page)
        self.stacked.addWidget(self.overview_page)

        #layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.navbar)
        main_layout.addWidget(self.stacked)
        self.setLayout(main_layout)

        #nav connections
        self.home_button.clicked.connect(self.show_home_page)
        self.add_button.clicked.connect(self.show_add_investment_page)
        self.overview_button.clicked.connect(self.show_portfolio_overview_page)

        self.compound_page = self.create_compound_interest_page()
        self.stacked.addWidget(self.compound_page)

        #nav button
        self.compound_button = QPushButton("Compound Interest")
        self.navbar.addWidget(self.compound_button)
        self.compound_button.clicked.connect(self.show_compound_interest_page)

        self.portfolio_list = []

    #home page
    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Investment Portfolio Tracker"))

        layout.addWidget(QLabel("Notification Threshold (£):"))
        self.threshold_input = QLineEdit("100")
        layout.addWidget(self.threshold_input)

        self.check_button = QPushButton("Check Notifications")
        layout.addWidget(self.check_button)
        self.check_button.clicked.connect(self.check_notifications)

        self.notify_label = QLabel("")
        layout.addWidget(self.notify_label)

        page.setLayout(layout)
        return page

    #investments page
    def create_add_investment_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("AlphaVantage API Key: "))
        self.api_key_input = QLineEdit()
        layout.addWidget(self.api_key_input)

        layout.addWidget(QLabel("Stock Ticker: "))
        self.ticker_input = QLineEdit()
        layout.addWidget(self.ticker_input)

        self.fetch_price_button = QPushButton("Fetch Latest Price")
        layout.addWidget(self.fetch_price_button)
        self.fetch_price_button.clicked.connect(self.fetch_current_price)

        layout.addWidget(QLabel("Buy Price: "))
        self.buy_input = QLineEdit()
        layout.addWidget(self.buy_input)

        layout.addWidget(QLabel("Current Price: "))
        self.current_input = QLineEdit()
        layout.addWidget(self.current_input)

        layout.addWidget(QLabel("Quantity: "))
        self.quantity_input = QLineEdit()
        layout.addWidget(self.quantity_input)

        self.add_stock_button = QPushButton("Add Stock")
        layout.addWidget(self.add_stock_button)
        self.add_stock_button.clicked.connect(self.add_stock)

        self.save_button = QPushButton("Save Portfolio")
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_portfolio)

        self.load_button = QPushButton("Load Portfolio")
        layout.addWidget(self.load_button)
        self.load_button.clicked.connect(self.load_portfolio)

        self.export_button = QPushButton("Export Portfolio to pdf")
        layout.addWidget(self.export_button)
        self.export_button.clicked.connect(self.export_portfolio)

        page.setLayout(layout)
        return page

    #portfolio overview page
    def create_portfolio_overview_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Portfolio Overview Graph"))
        self.results_label = QLabel("Click to calculate your Profit/Loss")
        layout.addWidget(self.results_label)

        self.calculate_button = QPushButton("Calculate Profit/Loss")
        self.calculate_button.clicked.connect(self.update_portfolio_overview)
        layout.addWidget(self.calculate_button)

        page.setLayout(layout)
        return page

    #compound interest tool
    def create_compound_interest_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Compound Interest Calculator"))

        layout.addWidget(QLabel("Starting Amount (£): "))
        self.starting_input = QLineEdit()
        layout.addWidget(self.starting_input)

        layout.addWidget(QLabel("Annual Interest Rate (%): "))
        self.rate_input = QLineEdit()
        layout.addWidget(self.rate_input)

        layout.addWidget(QLabel("Years: "))
        self.years_input = QLineEdit()
        layout.addWidget(self.years_input)

        layout.addWidget(QLabel("Number of times compounded (per year):"))
        self.freq_input = QLineEdit("1")
        layout.addWidget(self.freq_input)

        self.calc_button = QPushButton("Calculate Compound Interest")
        layout.addWidget(self.calc_button)
        self.calc_button.clicked.connect(self.calculate_compound_interest)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        page.setLayout(layout)
        return page

    def calculate_compound_interest(self):
        try:
            P = float(self.starting_input.text())
            r = float(self.rate_input.text()) / 100
            t = float(self.years_input.text())
            n = float(self.freq_input.text())

            T = P * (1 + r / n) * (n * t) #standard comppound interest formula
            interest = A - P

            self.result_label.setText(f"Total Amount: £{T:.2f}\nInterest Earned: £{interest:.2f}")
        except ValueError:
            self.result_label.setText("Please enter values for each section")

    #nav bar functions
    def show_home_page(self):
        self.stacked.setCurrentWidget(self.home_page)

    def show_add_investment_page(self):
        self.stacked.setCurrentWidget(self.add_page)

    def show_portfolio_overview_page(self):
        self.stacked.setCurrentWidget(self.overview_page)

    def show_compound_interest_page(self):
        self.stacked.setCurrentWidget(self.compound_page)

    # add stock function
    def add_stock(self):
        try:
            ticker = self.ticker_input.text().strip()
            buy_price = float(self.buy_input.text())
            current_price = float(self.current_input.text())
            quantity = int(self.quantity_input.text())

            stock = {
                "ticker": ticker, "buy_price": buy_price, "current_price": current_price, "quantity": quantity
            }

            self.portfolio_list.append(stock)
            print("Stock added successfully")

        except ValueError:
            print("Enter a valid input please")

    #save & load portfolio data
    def save_portfolio(self):
        with open("portfolio.json", "w") as f:
            json.dump(self.portfolio_list, f)
        print("Portfolio saved successfully!")

    def load_portfolio(self):
        try:
            with open("portfolio.json", "r") as f:
                self.portfolio_list = json.load(f)
            print("Portfolio loaded successfully!")
        except FileNotFoundError:
            print("No saved portfolio found.")

    #calculate profit/loss for each stock
    def calculate_profit_loss(self):
        for stock in self.portfolio_list:
            try:
                buy_price = float(stock["buy_price"])
                current_price = float(stock["current_price"])
                quantity = int(stock["quantity"])
                profit_loss = (current_price - buy_price) * quantity
                stock["profit_loss"] = (profit_loss)
            except (ValueError, KeyError):
                stock["profit_loss"] = 0

    def calculate_total_portfolio_value(self):
        total = 0
        for stock in self.portfolio_list:
            total = total + float(stock["current_price"]) * int(stock["quantity"])
        return round(total, 2)

    def update_portfolio_overview(self):
        if not self.portfolio_list:
            self.results_label.setText("Add stocks first and retry")
            return

        self.calculate_profit_loss()
        total_value = self.calculate_total_portfolio_value()
        total_profit_loss = sum(stock["profit_loss"] for stock in self.portfolio_list)

        output = ""
        for stock in self.portfolio_list:
            output = output + (
                f"{stock['ticker']}: Buy £{stock['buy_price']:.2f}, "
                f"Current £{stock['current_price']:.2f}, "
                f"Quantity {stock['quantity']}, "
                f"Profit/Loss £{stock['profit_loss']:.2f}\n"
            )

        output += f"\nTotal Portfolio Value: £{total_value:.2f}\n"
        output += f"Overall Profit/Loss: £{total_profit_loss:.2f}"

        if total_profit_loss > 0:
            colour = "green"
        elif total_profit_loss < 0:
            colour = "red"
        else:
            colour = "grey"

        self.results_label.setText(output)
        self.results_label.setStyleSheet(f"color: {colour}")

        self.check_notifications()

    def check_notifications(self):
            if not self.portfolio_list:
                self.notify_label.setText("Add stocks first")
                return

            try:
                threshold = float(self.threshold_input.text())
            except:
                self.notify_label.setText("Enter a number you want to set as your threshold number")
                return

            self.calculate_profit_loss()
            total_profit_loss = sum(stock["profit_loss"] for stock in self.portfolio_list)

            if abs(total_profit_loss) > threshold:
                self.notify_label.setText(f"P/L £{total_profit_loss:.2f} exceeds your set threshold, act quickly!")
            else:
                self.notify_label.setText("No notifications yet")

    def Portfolio_Overview_Graph(self):
        json_data = {
            "Stocks": [self.portfolio_list],
            "Value": [self.portfolio_list]
        }
        plt.bar(json_data["Stocks"], json_data["Value"])
        plt.xlabel('Stocks')
        plt.ylabel('Value')
        plt.title('Portfolio Overview Graph')
        plt.show()

    def fetch_current_price(self):
        key = self.api_key_input.text().strip()
        symbol = self.ticker_input.text().strip().upper()

        if not key or not symbol:
            print("Missing API key or ticker")
            return

        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={key}"
            r = requests.get(url)
            data = r.json()
            price = data.get("Global Quote", {}).get("05. price")

            if price:
                self.current_input.setText(str(round(float(price), 2)))
                print(f"{symbol} price updated!")
            else:
                print("Invalid API response")

        except Exception as e:
            print("API Error:", e)

    def export_portfolio(self):
        if not self.portfolio_list:
            print("Add stocks first before exporting")
            return

        self.calculate_profit_loss()
        total_value = self.calculate_total_portfolio_value()
        total_profit_loss = sum(stock["profit_loss"] for stock in self.portfolio_list)

        text = "Investment Portfolio Report\n\n"

        for stock in self.portfolio_list:
            text += (
                f"{stock['ticker']} - Buy: £{stock['buy_price']:.2f}, "
                f"Current: £{stock['current_price']:.2f}, "
                f"Qty: {stock['quantity']}, "
                f"P/L: £{stock['profit_loss']:.2f}\n"
            )

        text += f"\nTotal Portfolio Value: £{total_value:.2f}\n"
        text += f"Overall Profit/Loss: £{total_profit_loss:.2f}\n"

        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName("portfolio_report.pdf")

        doc = QTextDocument()
        doc.setPlainText(text)
        doc.print_(printer)

        print("Portfolio exported as portfolio_report.pdf")


#main exec
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())