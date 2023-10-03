"""Layout lookups.

List of lookups for reference to dashapp
"""
from dash.dash_table.Format import Format, Scheme

# set up lists
USexchanges = [
    "NASDAQ",
    "New York Stock Exchange",
]  # ,'US OTC', 'NYSE American' 'NASDAQ', 'New York Stock Exchange'

list_sector = [
    "XLV",
    "XLK",
    "XLY",
    "XLP",
    "XLB",
    "XLI",
    "IYT",
    "RWR",
    "XLF",
    "XLU",
    "SPY",
]

# set up columns

quote_col = [
    "symbol",
    "companyName",
    "isUSMarketOpen",
    "latestPrice",
    "previousClose",
    "latestUpdate",
    "latestSource",
    "change",
    "changePercent",
    "ytdChange",
    "latestVolume",
    "avgTotalVolume",
    "previousVolume",
    "marketCap",
    "peRatio",
    "extendedPrice",
    "extendedPriceTime",
    "open",
    "close",
    "high",
    "low",
    "week52High",
    "week52Low",
]

yahoo_info = {
    "info": [
        "address1",
        "city",
        "state",
        "zip",
        "country",
        "phone",
        "website",
        "industry",
        "industryDisp",
        "sector",
        "sectorDisp",
        # "longBusinessSummary",
        "fullTimeEmployees",
        # "companyOfficers",
        "exchange",
        "quoteType",
        "symbol",
        "underlyingSymbol",
        "shortName",
        "longName",
        "firstTradeDateEpochUtc",
        "timeZoneFullName",
        "timeZoneShortName",
        "uuid",
        "messageBoardId",
        "gmtOffSetMilliseconds",
        "exDividendDate",
    ],
    "risk": [
        "auditRisk",
        "boardRisk",
        "compensationRisk",
        "shareHolderRightsRisk",
        "overallRisk",
        "governanceEpochDate",
        "compensationAsOfEpochDate",
        "maxAge",
    ],
    "quote": [
        "priceHint",
        "previousClose",
        "open",
        "dayLow",
        "dayHigh",
        "regularMarketPreviousClose",
        "regularMarketOpen",
        "regularMarketDayLow",
        "regularMarketDayHigh",
        "payoutRatio",
        "beta",
        "trailingPE",
        "forwardPE",
        "volume",
        "regularMarketVolume",
        "averageVolume",
        "averageVolume10days",
        "averageDailyVolume10Day",
        "bid",
        "ask",
        "bidSize",
        "askSize",
        "marketCap",
        "fiftyTwoWeekLow",
        "fiftyTwoWeekHigh",
        "priceToSalesTrailing12Months",
        "fiftyDayAverage",
        "twoHundredDayAverage",
        "trailingAnnualDividendRate",
        "trailingAnnualDividendYield",
        "currency",
        "enterpriseValue",
        "profitMargins",
        "floatShares",
        "sharesOutstanding",
        "sharesShort",
        "sharesShortPriorMonth",
        "sharesShortPreviousMonthDate",
        "dateShortInterest",
        "sharesPercentSharesOut",
        "heldPercentInsiders",
        "heldPercentInstitutions",
        "shortRatio",
        "shortPercentOfFloat",
        "impliedSharesOutstanding",
        "bookValue",
        "priceToBook",
        "lastFiscalYearEnd",
        "nextFiscalYearEnd",
        "mostRecentQuarter",
        "earningsQuarterlyGrowth",
        "netIncomeToCommon",
        "trailingEps",
        "forwardEps",
        "pegRatio",
        "lastSplitFactor",
        "lastSplitDate",
        "enterpriseToRevenue",
        "enterpriseToEbitda",
        "52WeekChange",
        "SandP52WeekChange",
        "currentPrice",
    ],
    "analyst": [
        "targetHighPrice",
        "targetLowPrice",
        "targetMeanPrice",
        "targetMedianPrice",
        "recommendationMean",
        "recommendationKey",
        "numberOfAnalystOpinions",
    ],
    "fundamental": [
        "totalCash",
        "totalCashPerShare",
        "ebitda",
        "totalDebt",
        "quickRatio",
        "currentRatio",
        "totalRevenue",
        "debtToEquity",
        "revenuePerShare",
        "returnOnAssets",
        "returnOnEquity",
        "grossProfits",
        "freeCashflow",
        "operatingCashflow",
        "earningsGrowth",
        "revenueGrowth",
        "grossMargins",
        "ebitdaMargins",
        "operatingMargins",
        "financialCurrency",
        "trailingPegRatio",
    ],
}

# set up table formats
active_fmt = [
    dict(id="symbol", name="symbol"),
    dict(id="name", name="name"),
    dict(
        id="price_intraday",
        name="price_intraday",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="change",
        name="change",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="%_change",
        name="%_change",
        type="numeric",
        format=Format(precision=0, scheme=Scheme.percentage),
    ),
    dict(
        id="volume",
        name="volume",
        type="numeric",
        format=Format(precision=0, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="avg_vol_3_month",
        name="avg_vol_3_month",
        type="numeric",
        format=Format(precision=0, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="market_cap",
        name="market_cap",
        type="numeric",
        format=Format(precision=0, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="vol_delta",
        name="vol_delta",
        type="numeric",
        format=Format(precision=0, scheme=Scheme.percentage),
    ),
    dict(
        id="vol_price",
        name="vol_price",
        type="numeric",
        format=Format(precision=0, scheme=Scheme.fixed).group(True),
    ),
]

performance_fmt = [
    dict(id="ticker", name="ticker"),
    dict(id="date", name="date"),
    dict(id="lookback_date", name="lookback_date"),
    dict(
        id="average_price",
        name="average_price",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="last_price",
        name="last_price",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="cumulative_units",
        name="cumulative_units",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="cumulative_cost",
        name="cumulative_cost",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="market_value",
        name="market_value",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="return",
        name="return",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="dwrr_pct",
        name="dwrr_pct",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.percentage),
    ),
    dict(
        id="dwrr_ann_pct",
        name="dwrr_ann_pct",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.percentage),
    ),
    dict(
        id="realized",
        name="realized",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="unrealized",
        name="unrealized",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
]

transactions_fmt = [
    dict(
        id="date",
        name="date",
    ),
    dict(
        id="ticker",
        name="ticker",
    ),
    dict(
        id="type",
        name="type",
    ),
    dict(
        id="units",
        name="units",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="cost",
        name="cost",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
    dict(
        id="broker",
        name="broker",
    ),
    dict(
        id="price",
        name="price",
        type="numeric",
        format=Format(precision=2, scheme=Scheme.fixed).group(True),
    ),
]
