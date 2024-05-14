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
### Regression test for consistency of hour data over a reverse split event in US equities.
### </summary>
### <meta name="tag" content="using data" />
### <meta name="tag" content="regression test" />
class HourReverseSplitRegressionAlgorithm(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2013, 11, 7)
        self.set_end_date(2013, 11, 8)
        self.set_cash(100000)
        self.set_benchmark(lambda x: 0)

        self._symbol = self.add_equity("VXX.1", Resolution.HOUR).symbol
    
    def on_data(self, slice):
        if slice.bars.count == 0: return
        if (not self.portfolio.invested) and self.time.date() == self.end_date.date():
            self.buy(self._symbol, 1)
