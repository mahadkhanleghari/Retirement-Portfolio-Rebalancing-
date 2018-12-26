import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import csv
class RetirementSavings:

    def __init__(self):
        self.categories = ["Cash", "Bank Savings", "Bond Investments", "Stock Investments"]
        self.years_to_retirement = 0
        self.investment = 0
        self.annual_increase = 0
        self.bank_savings_return = 0.02
        self.cash_inflation = -0.06
        self.starting_percentages = {}
        self.ending_percentages = {}
        self.target_percentages_increment = {}
        self.cash_savings = 0
        self.bank_savings = 0
        self.bond_savings = 0
        self.stock_savings = 0
        self.stocks_historical = []
        self.bonds_historical = []
        self.cash_future = []
        self.bank_future = []
        self.stocks_future = []
        self.bonds_future = []
        self.portfolio = []
        self.investment_per_year = {}
        self.num_years = []

    def get_user_input(self):
        self.years_to_retirement = int(input('How many years to retirement?:\n'))
        self.investment = int(input("How much are willing to invest right now?: \n"))
        self.annual_increase = float(input("How much will you increase your annual investment by in %%?: \n")) / 100
        self.cash_savings = int(input("How much are your cash savings at this moment?: \n"))
        self.bank_savings = int(input("How much are your bank savings at this moment?: \n"))
        self.bond_savings = int(input("How much are your bond savings at this moment?: \n"))
        self.stock_savings = int(input("How much are your stock savings at this moment?: \n"))


    def start_percentages(self):
        remaining = 1
        for category in self.categories:
            self.starting_percentages[category] = float(input("What starting percentage do you want for %s " % category))/100
            remaining = remaining - self.starting_percentages[category]
            new = remaining * 100
            print("You have", new, " % left to invest")


    def end_percentages(self):
        endremaining = 1
        for category in self.categories:
            self.ending_percentages[category] = float(input("What ending percentage do you want for %s" % category))/100
            endremaining = endremaining - self.ending_percentages[category]
            endnew = endremaining * 100
            print("You have", endnew, " % left to invest")


    def target_allocation(self, ending_categories):
        for category in self.categories:
            increment = (ending_categories[category] - self.starting_percentages[category])/(self.years_to_retirement)
            self.target_percentages_increment[category] = increment

    def historical_returns(self):
        with open("bonds.txt", "r") as bonds_file:
            bond_values = bonds_file.readlines()
            for b_value in bond_values:
                self.bonds_historical.append(float(b_value))
        with open("stocks.txt", "r") as stocks_file:
            stock_values = stocks_file.readlines()
            for s_value in stock_values:
                self.stocks_historical.append(float(s_value))

    def investment_peryear(self):
        cumulative_investment = self.investment
        for years in range(self.years_to_retirement+1):
            self.investment_per_year[years] = cumulative_investment
            cumulative_investment *= 1 + self.annual_increase
        return self.investment_per_year


    def future_returns(self):
        total_portfolio = self.cash_savings + self.bank_savings + self.bond_savings + self.stock_savings
        actual_year_portfolio = 0
        actual_portfolio_percentage_year = {"Cash": 0, "Bank": 0, "Stocks": 0, "Bonds": 0}
        rebalanced_portfolio_percentage_year = {"Cash": 0, "Bank": 0, "Stocks": 0, "Bonds": 0}
        for years in range(1, self.years_to_retirement + 1):
            category_amount = []
            for category in self.categories:
                investment_for_year = self.investment * ((1 + self.annual_increase)**years)
                if category == "Cash":
                    target_percent_year = self.starting_percentages[category] + \
                                          (years * self.target_percentages_increment[category])
                    investment_category = investment_for_year * target_percent_year
                    savings_on_investment = investment_category * ((1 + self.cash_inflation)**years)
                    category_amount.append(savings_on_investment)
                    actual_year_portfolio += savings_on_investment

                elif category == "Bank Savings":
                    bstarget_percent_year = self.starting_percentages[category] + \
                                          (years * self.target_percentages_increment[category])
                    bsinvestment_category = investment_for_year * bstarget_percent_year
                    bssavings_on_investment = bsinvestment_category * ((1 + self.bank_savings_return)**years)
                    category_amount.append(bssavings_on_investment)
                    actual_year_portfolio += bssavings_on_investment


                elif category == "Stock Investments":
                    starget_percent_year = self.starting_percentages[category] + \
                                          (years * self.target_percentages_increment[category])
                    sinvestment_category = investment_for_year * starget_percent_year
                    ssavings_on_investment = sinvestment_category * (1 + self.stocks_historical[years])
                    category_amount.append(ssavings_on_investment)
                    actual_year_portfolio += ssavings_on_investment


                elif category == "Bond Investments":
                    btarget_percent_year = self.starting_percentages[category] + \
                                           (years * self.target_percentages_increment[category])
                    binvestment_category = investment_for_year * (btarget_percent_year)
                    bsavings_on_investment = binvestment_category * (1 + self.bonds_historical[years])
                    category_amount.append(bsavings_on_investment)
                    actual_year_portfolio += bsavings_on_investment

            total_portfolio += actual_year_portfolio

            actual_portfolio_percentage_year["Cash"] = (category_amount[0] + self.cash_savings)/total_portfolio
            actual_portfolio_percentage_year["Bank"] = (category_amount[1] + self.bank_savings)/total_portfolio
            actual_portfolio_percentage_year["Bonds"] = (category_amount[2] + self.bond_savings)/total_portfolio
            actual_portfolio_percentage_year["Stocks"] = (category_amount[3] + self.stock_savings) / total_portfolio

            #rebalance
            self.cash_savings = (self.starting_percentages["Cash"] + \
                                           (years * self.target_percentages_increment["Cash"])) * total_portfolio
            self.bank_savings = (self.starting_percentages["Bank Savings"] + \
                                           (years * self.target_percentages_increment["Bank Savings"])) * total_portfolio
            self.bond_savings = (self.starting_percentages["Bond Investments"] + \
                                           (years * self.target_percentages_increment["Bond Investments"])) * total_portfolio
            self.stock_savings = (self.starting_percentages["Stock Investments"] + \
                                           (years * self.target_percentages_increment["Stock Investments"])) * total_portfolio

            rebalanced_portfolio_percentage_year["Cash"] = (self.cash_savings) / total_portfolio
            rebalanced_portfolio_percentage_year["Bank"] = (self.bank_savings) / total_portfolio
            rebalanced_portfolio_percentage_year["Bonds"] = (self.bond_savings) / total_portfolio
            rebalanced_portfolio_percentage_year["Stocks"] = (self.stock_savings) / total_portfolio


            rounded_cash = round(self.cash_savings, 1)
            rounded_bank = round(self.bank_savings, 1)
            rounded_bond = round(self.bond_savings, 1)
            rounded_stock = round(self.stock_savings, 1)
            rounded_port = round(total_portfolio, 1)


            self.cash_future.append(rounded_cash)
            self.bank_future.append(rounded_bank)
            self.bonds_future.append(rounded_bond)
            self.stocks_future.append(rounded_stock)
            self.portfolio.append(rounded_port)

    def number_of_years(self):
        for years in range(1,self.years_to_retirement+1):
            self.num_years.append(years)



    def file_csv(self):
        revised_cat_list = ["Cash", "Bank Savings", "Stock Investments", "Bond Investments"]
        file_name = "retirementsimulation.csv"
        portfolio_heading = "Portfolio Value"
        year_heading = "Years"
        with open(file_name, 'w') as output_file:
            sim_writer = csv.writer(output_file)
            heading_y = [year_heading] + self.num_years
            sim_writer.writerow(heading_y)
            heading = [portfolio_heading] + self.portfolio
            sim_writer.writerow(heading)
            for cat in revised_cat_list:
                if cat == "Cash":
                    cash_list = [cat] + self.cash_future
                    sim_writer.writerow(cash_list)
                elif cat == "Bank Savings":
                    bank_list = [cat] + self.bank_future
                    sim_writer.writerow(bank_list)
                elif cat == "Stock Investments":
                    stock_list = [cat] + self.stocks_future
                    sim_writer.writerow(stock_list)
                elif cat == "Bond Investments":
                    bond_list = [cat] + self.bonds_future
                    sim_writer.writerow(bond_list)

    def plotting(self):
        plt.title("Portfolio Value")
        plt.plot(self.num_years, self.portfolio, label = "Portfolio")
        plt.plot(self.num_years, self.cash_future, label = "Cash")
        plt.plot(self.num_years, self.bank_future, label = "Bank Savings")
        plt.plot(self.num_years, self.bonds_future, label = "Bonds")
        plt.plot(self.num_years, self.stocks_future, label = "Stocks")
        plt.xlabel("Years")
        plt.ylabel("Value")
        plt.legend()
        plt.show()


#create an independent function
def plot_comparisons(numyears, port1, port2, port3, port4):
    plt.title("Relative Portfolio Value ")
    plt.plot(numyears, port1, label="Your Portfolio")
    plt.plot(numyears, port2, label="Portfolio via Stocks Ending at 70%")
    plt.plot(numyears, port3, label="Portfolio via Bonds Ending at 70%")
    plt.plot(numyears, port4, label="Portfolio via Bank Savings Ending at 70%")
    plt.xlabel("Years")
    plt.ylabel("Value")
    plt.legend()
    plt.show()







































