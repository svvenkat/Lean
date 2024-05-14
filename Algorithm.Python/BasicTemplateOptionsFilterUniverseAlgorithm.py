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
### This example demonstrates how to add options for a given underlying equity security.
### It also shows how you can prefilter contracts easily based on strikes and expirations.
### It also shows how you can inspect the option chain to pick a specific option contract to trade.
### </summary>
### <meta name="tag" content="using data" />
### <meta name="tag" content="options" />
### <meta name="tag" content="filter selection" />
class BasicTemplateOptionsFilterUniverseAlgorithm(QCAlgorithm):
    underlying_ticker = "GOOG"

    def initialize(self):
        self.set_start_date(2015, 12, 24)
        self.set_end_date(2015, 12, 28)
        self.set_cash(100000)

        equity = self.add_equity(self.underlying_ticker)
        option = self.add_option(self.underlying_ticker)
        self.option_symbol = option.symbol

        # Set our custom universe filter
        option.set_filter(self.filter_function)

        # use the underlying equity as the benchmark
        self.set_benchmark(equity.symbol)

    def filter_function(self, universe):
        #Expires today, is a call, and is within 10 dollars of the current price
        universe = universe.weeklys_only().expiration(0, 1)
        return [symbol for symbol in universe 
                if symbol.id.option_right != OptionRight.PUT 
                and -10 < universe.underlying.price - symbol.id.strike_price < 10]

    def on_data(self, slice):
        if self.portfolio.invested: return

        for kvp in slice.option_chains:
            
            if kvp.key != self.option_symbol: continue

            # Get the first call strike under market price expiring today
            chain = kvp.value
            contracts = [option for option in sorted(chain, key = lambda x:x.strike, reverse = True)
                         if option.expiry.date() == self.time.date()
                         and option.strike < chain.underlying.price]
            
            if contracts:
                self.market_order(contracts[0].symbol, 1)
