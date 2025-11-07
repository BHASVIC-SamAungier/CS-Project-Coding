import plt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QStackedWidget)

import sys
import json
import matplotlib

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

        self.portfolio_list = []

    #home page
    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Investment Portfolio Tracker"))
        page.setLayout(layout)
        return page

    #investments page
    def create_add_investment_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Stock Ticker: "))
        self.ticker_input = QLineEdit()
        layout.addWidget(self.ticker_input)

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
        self.save_button = QPushButton("Save Portfolio")
        self.load_button = QPushButton("Load Portfolio")
        layout.addWidget(self.add_stock_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        self.add_stock_button.clicked.connect(self.add_stock)
        self.save_button.clicked.connect(self.save_portfolio)
        self.load_button.clicked.connect(self.load_portfolio)

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

    #nav bar functions
    def show_home_page(self):
        self.stacked.setCurrentWidget(self.home_page)

    def show_add_investment_page(self):
        self.stacked.setCurrentWidget(self.add_page)

    def show_portfolio_overview_page(self):
        self.stacked.setCurrentWidget(self.overview_page)

    #add stock function
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

        







#main exec
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())