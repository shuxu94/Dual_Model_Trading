__author__ = 'shuxu'

import matplotlib.pyplot as plt
import urllib2
import dateutil.parser


class RiskAversion:
    def __init__(self, time_horizon):
        """creates the risk aversion object"""
        self.time_horizon = time_horizon
        self.array_size = 10001
        self.sample_size = 0
        self.freq_dist = [0] * self.array_size # 13.32% would be index 1332
        self.freq_lookup = [0] * self.array_size
        self.vix_url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv'
        self.response = urllib2.urlopen(self.vix_url)
        self.build_freq_lookup_table()

    def get_beta(self, current_vix):
        """gets the current beta value the portfolio should have"""
        #TODO do the mapping here
        return 1.3 - self.freq_lookup[int(current_vix*100)]

    def print_graphs(self):
        # plt.plot(range(self.array_size), self.freq_dist)
        # plt.title('Frequency Distribution of VIX from 2003 - Present')
        # plt.ylabel('Number of occurrence')
        # plt.xlabel('^VIX * 100')
        # plt.savefig('freq_dist.png')
        plt.plot(range(self.array_size), self.freq_lookup)
        plt.ylabel('Percentile')
        plt.xlabel('^VIX * 100')
        plt.savefig('freq_lookup.png')

    def get_historicalVIX(self):
        """gets the historical ^VIX data from CBOE website"""
        self.response = urllib2.urlopen(self.vix_url)

    # how much to weight data from the past
    def get_frequency_weight(self, date):
        #TODO implement a more sophisticated weight system
        weight = date.year - 2010
        if (weight < 0):
            weight = 1
        return weight


    def build_freq_distribution(self):
        """builds the frequency Distribution"""
        self.get_historicalVIX()
        # skip the first 2 lines
        for _ in xrange(2):
            next(self.response)
        # parse input line by line and build freq dist
        # min = 9.89
        # max = 80.86
        for line in self.response.readlines():
            # in index 0 is the date in index 4 is closing price which we will use
            s = line.split(',')
            # parses the date in csv from string to datetime object
            date = dateutil.parser.parse(s[0]);
            # the ^VIX value is used as the index in the list
            i = int(float(s[4][:-2])*100)

            # increment the count and insert back into the freq distribution
            count = self.freq_dist[i]
            count += 1 * self.get_frequency_weight(date)
            self.freq_dist[i] = count
            # keep track of how many samples we have
            self.sample_size += self.get_frequency_weight(date)

    def build_freq_lookup_table(self):
        """builds the frequency lookup table"""
        self.build_freq_distribution()
        running_sum = 0

        for i in xrange(self.array_size):
            self.freq_lookup[i] = float(running_sum)/float(self.sample_size);
            running_sum += self.freq_dist[i]

    def update_beta(self):
        """updates the current beta"""
        self.build_freq_lookup_table()



def main():
    ra = RiskAversion(5);
    ra.build_freq_lookup_table();
    ra.print_graphs();

if __name__ == "__main__":
    main()