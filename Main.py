from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QStackedWidget

import sys
import json


class MainWindow(QWidget):  # main window class
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Investment Portfolio Tracker")

        #nav bar
        self.navbar = QHBoxLayout()
        self.home_button = QPushButton("Home")
        self.add_button = QPushButton("Add Investment")
        self._button = QPushButton("")
        self.navbar.addWidget(self.home_button)
        self.navbar.addWidget(self.add_button)

        #stacked paegs
        self.stacked = QStackedWidget()
        self.home_page = self.create_home_page()
        self.add_page = self.create_add_investment_page()
        self.stacked.addWidget(self.home_page)
        self.stacked.addWidget(self.add_page)

        #layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.navbar)
        main_layout.addWidget(self.stacked)
        self.setLayout(main_layout)

        #nav bar connections
        self.home_button.clicked.connect(self.show_home_page)
        self.add_button.clicked.connect(self.show_add_investment_page)

        #decleaing portfolio list
        self.portfolio_list = []

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to your Investment Portfolio Tracker"))
        page.setLayout(layout)
        return page

    #adding investments
    def create_add_investment_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Stock Ticker: "))
        self.ticker_input = QLineEdit()
        layout.addWidget(self.ticker_input)

        layout.addWidget(QLabel("Buy Price (DO NOT INCLUDE £): "))
        self.buy_input = QLineEdit()
        layout.addWidget(self.buy_input)

        layout.addWidget(QLabel("Current Price (DO NOT INCLUDE £): "))
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

    #page switching
    def show_home_page(self):
        self.home_page.show()
        self.add_page.hide()

    def show_add_investment_page(self):
        self.add_page.show()
        self.home_page.hide()

    #adding a stock
    def add_stock(self):
        try:
            ticker = self.ticker_input.text()
            buy_price = float(self.buy_input.text())
            current_price = float(self.current_input.text())
            quantity = int(self.quantity_input.text())

            if not ticker or buy_price <= 0 or quantity <= 0:
                return ValueError

            stock = {"ticker": ticker, "buy_price": buy_price, "current_price": current_price, "quantity": quantity}
            self.portfolio_list.append(stock)
            print("Stock added successfully!")
        except ValueError:
            print("Invalid input try again")

    def save_portfolio(self):
        with open("portfolio.json", "w") as f:  # tut for this - cite
            json.dump(self.portfolio_list, f)  # tut for this - cite
        print("Portfolio saved successfully!")

    def load_portfolio(self):
        try:
            with open("portfolio.json", "r") as f:  # tut for this - cite
                self.portfolio_list = json.load(f)  # tut for this - cite
            print("Portfolio loaded successfully!")
        except FileNotFoundError:
            print("No saved portfolio found")


if __name__ == "__main__":  # tut for this - cite
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
