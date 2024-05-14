# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from AlgorithmImports import *

### <summary>
### In this example we look at the canonical 15/30 day moving average cross. This algorithm
### will go long when the 15 crosses above the 30 and will liquidate when the 15 crosses
### back below the 30.
### </summary>
### <meta name="tag" content="indicators" />
### <meta name="tag" content="indicator classes" />
### <meta name="tag" content="moving average cross" />
### <meta name="tag" content="strategy example" />
class MovingAverageCrossAlgorithm(QCAlgorithm):

    def initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        self.set_start_date(2009, 1, 1)    #Set Start Date
        self.set_end_date(2015, 1, 1)      #Set End Date
        self.set_cash(100000)             #Set Strategy Cash
        # Find more symbols here: http://quantconnect.com/data
        self.add_equity("SPY")

        # create a 15 day exponential moving average
        self.fast = self.ema("SPY", 15, Resolution.DAILY)

        # create a 30 day exponential moving average
        self.slow = self.ema("SPY", 30, Resolution.DAILY)

        self.previous = None


    def on_data(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''
        # a couple things to notice in this method:
        #  1. We never need to 'update' our indicators with the data, the engine takes care of this for us
        #  2. We can use indicators directly in math expressions
        #  3. We can easily plot many indicators at the same time

        # wait for our slow ema to fully initialize
        if not self.slow.is_ready:
            return

        # only once per day
        if self.previous is not None and self.previous.date() == self.time.date():
            return

        # define a small tolerance on our checks to avoid bouncing
        tolerance = 0.00015

        holdings = self.portfolio["SPY"].quantity

        # we only want to go long if we're currently short or flat
        if holdings <= 0:
            # if the fast is greater than the slow, we'll go long
            if self.fast.current.value > self.slow.current.value *(1 + tolerance):
                self.log("BUY  >> {0}".format(self.securities["SPY"].price))
                self.set_holdings("SPY", 1.0)

        # we only want to liquidate if we're currently long
        # if the fast is less than the slow we'll liquidate our long
        if holdings > 0 and self.fast.current.value < self.slow.current.value:
            self.log("SELL >> {0}".format(self.securities["SPY"].price))
            self.liquidate("SPY")

        self.previous = self.time
