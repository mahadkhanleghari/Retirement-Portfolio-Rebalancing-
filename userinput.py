def get_user_input(self):
    self.years_to_retirement = int(input('How many years to retirement?:\n'))
    self.investment = int(input("How much are willing to invest right now?: \n"))
    self.annual_increase = float(input("How much will you increase your annual investment by?: \n")) / 100
    self.cash_savings = int(input("How much are your cash savings at this moment?\n"))
    self.bank_savings = int(input("How much are your bank savings at this moment?\n"))
    self.bond_savings = int(input("How much are your bond savings at this moment?\n"))
    self.stock_savings = int(input("How much are your stock savings at this moment?\n"))
    self.portfolio = self.cash_savings + self.bank_savings + self.bond_savings + self.stock_savings


    def start_percentages(self):
        for category in self.categories:
            self.starting_percentages[category] = float(input("What starting %% do you want for %s " % category))/100

    def end_percentages(self):
        for category in self.categories:
            self.ending_percentages[category] = float(input("What ending %% do you want for %s" % category))/100