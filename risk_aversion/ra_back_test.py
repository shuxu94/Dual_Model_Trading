__author__ = 'shuxu'

import dateutil.parser
import risk_aversion as ra
import logging

y_url = "http://ichart.finance.yahoo.com/table.csv?s=SPY&a=0&b=1&c=2005&d=11&e=31&f=2014&g=w&ignore=.csv"
market_data = list()

class Portfolio:
    def __init__(self, starting_capital):

        # financials
        self.cash = starting_capital # amount of cash to start with
        self.equity = {'SPY': 0.0} #what stocks do i own
        self.liquidation_value = starting_capital
        self.profits_total = 0.0 # total earnings
        self.profits_record = list() # list of all earnings when rebalanced
        self.portfolio_value_record = list()

        # practical parameters

        # risk algo param
        self.beta = 0.0;
        self.trading_horizon = 2 # number of weeks
        self.risk_aglo = ra.RiskAversion(self.trading_horizon)# assets marked to market aka liquidation value
        self.risk_aglo.build_freq_lookup_table()

        # takes in a row of market data and rebalances portfolio
    def rebalance_spy(self, current_data):
        logging.debug('Entering function rebalance_spy')
        # in current_data its date, vix, spy, sp500
        c_sp500 = float(current_data[3])
        c_spy_price = float(current_data[2])
        c_vix = float(current_data[1])
        c_date = current_data[0]

        ideal_beta = self.risk_aglo.get_beta(c_vix)
        ideal_spy_mtm = ideal_beta * self.liquidation_value  # value of spy we should have
        # check to see if difference between ideal and current is bigger than current spy price

        logging.info('Date: ' + str(c_date) + ' idea beta: ' + str(ideal_beta))

        difference_to_ideal = ideal_spy_mtm - self.equity['SPY']*c_spy_price

        if abs(difference_to_ideal) > c_spy_price:
            # if yes need to sell or buy SPY shares
            if difference_to_ideal > 0:
                # need to buy
                logging.info('rebalance asked to Buying SPY')
                buy_amount = int(difference_to_ideal/c_spy_price)

                logging.info('Need to buy ' + str(buy_amount) + ' of SPY')
                self.buy_spy(buy_amount)

            else:
                # need to sell
                logging.info('rebalance asked to Selling SPY')
                sell_amount = int(abs(difference_to_ideal)/c_spy_price)

                logging.info('Need to buy ' + str(sell_amount) + ' of SPY')
                self.sell_spy(sell_amount)



    def buy_spy(self, spy_ask, amount):

        buy_total = (spy_ask * amount) + self.transaction_fee(amount)
        if (self.cash < buy_total):
            print "insufficient cash to buy SPY order cancelled"
            return
        self.cash -= buy_total
        self.equity['SPY'] += amount

    def sell_spy(self, spy_bid, amount):
        sell_total = spy_bid * amount - self.transaction_fee(amount)
        self.cash += sell_total
        self.equity['SPY'] -= amount

    # calculate the transactional fee
    def transaction_fee(self, amount):
        return 10

def format():
    vix_file = open('../data/vix.csv')
    spy_file = open('../data/spy.csv')
    sp500_file = open('../data/sp500.csv')

    # skips the first line which is the column names
    vix_file.readline()
    spy_file.readline()
    sp500_file.readline()


    for vix, spy, sp500 in zip(vix_file.readlines(), spy_file.readlines(), sp500_file.readlines()):
        vix_parts = vix.split(',')
        spy_parts = spy.split(',')
        sp500_parts = sp500.split(',')
        row = list()
        date = dateutil.parser.parse(vix_parts[0])
        row.append(date);row.append(vix_parts[1])
        row.append(spy_parts[1]);row.append(sp500_parts[1])
        market_data.append(row)





def main():
    logging.basicConfig(level=logging.INFO)
    format()
    test_p1 = Portfolio(10000.0)
    test_p1.rebalance_spy(market_data[0]);


if __name__ == "__main__":
    main()