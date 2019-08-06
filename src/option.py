"""
Created on Fri Apr 19 2019
Description: Derivatives Pricing Calculator

@author: Siping Wang
"""
import numpy as np
import scipy.stats as sps
import math


class Option(object):
    def __init__(self, type, s0, sp, maturity, rf, v, i):
        # initialize the type of option (call/put)
        if type == 'Call':
            self.type = 1.0
        else:
            self.type = -1.0

        # initialize the essential variables for pricing options
        self.s0 = s0 * 1.0
        self.sp = sp * 1.0
        self.maturity = maturity * 1.0
        self.rf = rf * 1.0
        self.v = v * 1.0
        self.i = i * 1.0

        # initialize the price of two methods (private members)
        self.__bsprice = 0.0
        self.__mcprice = 0.0

    def BlackScholesPricing(self):
        # use Black-Scholes formula
        d1 = ((math.log (self.s0 / self.sp) + self.maturity * (0.5 * self.v * self.v + self.rf - self.i))) / \
             (self.v * math.sqrt(self.maturity))
        d2 = d1 - self.v * math.sqrt(self.maturity)
        self.__bsprice = self.type * self.s0 * np.exp(-self.i * self.maturity) * sps.norm.cdf(self.type * d1) - \
                    self.type * self.sp * np.exp(-self.rf * self.maturity) * sps.norm.cdf(self.type * d2)
        return self.__bsprice

    def MonteCarloPricing(self, iteration=1000000):
        # use Monte Carlo simulation
        z_t = np.random.normal(0, 1, iteration)
        S_T = self.s0 * np.exp((self.rf - self.i - 0.5 * self.v * self.v) * self.maturity + \
                               self.v * math.sqrt(self.maturity) * z_t)
        mclist = []
        for s_T in S_T:
            mclist.append(max(self.type * (s_T - self.sp), 0))
        self.__mcprice = np.average(mclist) * np.exp(-self.rf * self.maturity)
        return self.__mcprice


# test
if __name__ == '__main__':
    option = Option('Call', 50, 50, 1, 0.02, 0.05, 0)
    print(option.type)
    print(option.maturity)
    print("\n")
    print("priced by Black-Scholes:")
    print(option.BlackScholesPricing())
    print("\n")
    print("priced by Monte Carlo:")
    for _ in range(10):
        print(option.MonteCarloPricing(100000))