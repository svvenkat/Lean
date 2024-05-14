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
### Regression algorithm used to test a fine and coarse selection methods returning Universe.UNCHANGED
### </summary>
class UniverseUnchangedRegressionAlgorithm(QCAlgorithm):

    def initialize(self):
        self.universe_settings.resolution = Resolution.DAILY

        # Order margin value has to have a minimum of 0.5% of Portfolio value, allows filtering out small trades and reduce fees.
        # Commented so regression algorithm is more sensitive
        #self.settings.minimum_order_margin_portfolio_percentage = 0.005
        self.set_start_date(2014,3,25)
        self.set_end_date(2014,4,7)

        self.set_alpha(ConstantAlphaModel(InsightType.PRICE, InsightDirection.UP, timedelta(days = 1), 0.025, None))
        self.set_portfolio_construction(EqualWeightingPortfolioConstructionModel())

        self.add_universe(self.coarse_selection_function, self.fine_selection_function)

        self.number_of_symbols_fine = 2

    def coarse_selection_function(self, coarse):
        # the first and second selection
        if self.time.date() <= date(2014, 3, 26):
            tickers = [ "AAPL", "AIG", "IBM" ]
            return [ Symbol.create(x, SecurityType.EQUITY, Market.USA) for x in tickers ]

        # will skip fine selection
        return Universe.UNCHANGED

    def fine_selection_function(self, fine):
        if self.time.date() == date(2014, 3, 25):
            sorted_by_pe_ratio = sorted(fine, key=lambda x: x.valuation_ratios.pe_ratio, reverse=True)
            return [ x.symbol for x in sorted_by_pe_ratio[:self.number_of_symbols_fine] ]

        # the second selection will return unchanged, in the following fine selection will be skipped
        return Universe.UNCHANGED

    # assert security changes, throw if called more than once
    def on_securities_changed(self, changes):
        added_symbols = [ x.symbol for x in changes.added_securities ]
        if (len(changes.added_securities) != 2
            or self.time.date() != date(2014, 3, 25)
            or Symbol.create("AAPL", SecurityType.EQUITY, Market.USA) not in added_symbols
            or Symbol.create("IBM", SecurityType.EQUITY, Market.USA) not in added_symbols):
            raise ValueError("Unexpected security changes")
        self.log(f"OnSecuritiesChanged({self.time}):: {changes}")
