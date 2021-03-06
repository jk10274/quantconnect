from QuantConnect.Data.Market import TradeBar


class RollingWindowAlgorithm(QCAlgorithm):
    '''Example on how to use Rolling Window with bar and indicator'''

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        self.SetStartDate(2013,10,1)  #Set Start Date
        self.SetEndDate(2013,11,1)    #Set End Date
        self.SetCash(100000)           #Set Strategy Cash
        # Find more symbols here: http://quantconnect.com/data
        self.AddEquity("SPY", Resolution.Daily)

        # Creates a Rolling Window indicator to keep the 2 TradeBar
        self.window = RollingWindow[TradeBar](2)    # For other security types, use QuoteBar

        # Creates an indicator and adds to a rolling window when it is updated        
        self.SMA("SPY", 5).Updated += self.SmaUpdated
        self.smaWin = RollingWindow[IndicatorDataPoint](5)


    def SmaUpdated(self, sender, updated):
        '''Adds updated values to rolling window'''
        self.smaWin.Add(updated)


    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''
        
        # Add SPY TradeBar in rollling window
        self.window.Add(data["SPY"])

        # Wait for windows to be ready.
        if not (self.window.IsReady and self.smaWin.IsReady): return

        currBar = self.window[0]                     # Current bar had index zero.
        pastBar = self.window[1]                     # Past bar has index one.
        self.Log("Price: {0} -> {1} ... {2} -> {3}".format(pastBar.Time, pastBar.Close, currBar.Time, currBar.Close))

        currSma = self.smaWin[0]                     # Current SMA had index zero.
        pastSma = self.smaWin[self.smaWin.Count-1]   # Oldest SMA has index of window count minus 1.
        self.Log("SMA:   {0} -> {1} ... {2} -> {3}".format(pastSma.Time, pastSma.Value, currSma.Time, currSma.Value))

        if not self.Portfolio.Invested and currSma.Value > pastSma.Value:
            self.SetHoldings("SPY", 1)
