/*
 * QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
 * Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/

using System;
using System.Linq;
using System.Drawing;
using NUnit.Framework;

namespace QuantConnect.Tests.Common
{
    [TestFixture]
    public class SeriesTests
    {
        [Test]
        public void RespectsMostRecentTimeOnDuplicatePoints()
        {
            var series = new Series();
            series.AddPoint(new DateTime(2023, 2, 2), 1m);
            series.AddPoint(new DateTime(2023, 2, 2), 2m);
            Assert.AreEqual(1, series.Values.Count);
            Assert.AreEqual(2m, series.GetValues<ChartPoint>().Single().y);
        }

        [TestCase(null, "toolTip")]
        [TestCase("IndexName", "toolTip")]
        [TestCase(null, null)]
        [TestCase("IndexName", null)]
        public void Clone(string indexName, string toolTip)
        {
            var series = new Series("A", SeriesType.Line, "TT", Color.AliceBlue, ScatterMarkerSymbol.Circle) { ZIndex = 98, Index = 8, IndexName = indexName, Tooltip = toolTip };
            var result = (Series)series.Clone();

            Assert.AreEqual(series.Name, result.Name);
            Assert.AreEqual(series.Unit, result.Unit);
            Assert.AreEqual(series.Tooltip, result.Tooltip);
            Assert.AreEqual(series.SeriesType, result.SeriesType);
            Assert.AreEqual(series.Color.ToArgb(), result.Color.ToArgb());
            Assert.AreEqual(series.ScatterMarkerSymbol, result.ScatterMarkerSymbol);
            Assert.AreEqual(series.Index, result.Index);
            Assert.AreEqual(series.ZIndex, result.ZIndex);
            Assert.AreEqual(series.IndexName, result.IndexName);
        }
    }
}
