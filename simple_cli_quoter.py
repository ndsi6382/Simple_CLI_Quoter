#!/usr/bin/env python3

import os, sys
import getopt
from datetime import datetime as dt
import yfinance as yf

CWD = os.getcwd()
EXCHANGES = {"ASX":".AX",
             "CBOT":".CBT",
             "CME":".CME",
             "COMEX":".CMX",
             "GLOBAL":"=X",
             "HKEX":".HK",
             "KOSDAQ":".KQ",
             "KSE":".KS",
             "NASDAQ":"",
             "NYMEX":".NYM",
             "NZX":".NZ",
             "OPRA":"",
             "SGX":".SI",
             "SIX":".SW",
             "SSE":".SS",
             "TSX":".TO",
             "TWSE":".TW"}

def quote(symbol, exchange, report, query):
    if exchange:
        try: symbol += EXCHANGES[exchange.upper()]
        except KeyError: pass
    symbol = symbol.upper()
    data = yf.Ticker(symbol).info
    output = ""
    fields = [*data.keys()]
    ignore = ['longName', 'shortName', 'name', 'symbol', 'description',
              'longBusinessSummary', 'logo_url', 'phone', 'address1', 'address2',
              'state', 'city', 'zip', 'fax', 'gmtOffSetMilliseconds', 'lastMarket',
              'maxAge', 'messageBoardId', 'market', 'fullTimeEmployees', 'twitter',
              'exchangeTimezoneName', 'exchangeTimezoneShortName', 'financialCurrency',
              'currentPrice', 'open', 'previousClose', 'dayHigh', 'dayLow']
               # ^ 'regularMarket' fields are used instead
    if len(fields) < 10:
        print("No data available for the given symbol! Please try a different input.")
        sys.exit(1)
    # Name
    if 'longName' in fields: output = f"{data['longName']} ({symbol})\n"
    else: output = f"{data['shortName']}\n"
    if query:
        for f in fields:
            if query.lower() == f.lower():
                print(output, end="")
                print(f"{f[0].upper()}{f[1:]}: {data[f]}")
                return
        print(f"Query field not found! Displaying full data for {symbol} instead...\n")
        quote(symbol, "", False, "")
        return
    # Introduction Fields
    output += "  ----  \n"
    if 'website' in fields: output += f"Website: {data.pop('website')}\n"
    if 'country' in fields: output += f"Country: {data.pop('country')}\n"
    if 'sector' in fields: output += f"Sector: {data.pop('sector')}\n"
    if 'industry' in fields: output += f"Industry: {data.pop('industry')}\n"
    if 'quoteType' in fields: output += f"Type: {data.pop('quoteType')}\n"
    if 'exchange' in fields: output += f"Exchange: {data.pop('exchange')}\n"
    if 'currency' in fields: output += f"Currency: {data.pop('currency')}\n"
    output += "  ----  \n"
    # "Priority" Details
    if 'regularMarketPrice' in fields:output += f"CurrentPrice: {data.pop('regularMarketPrice')}\n"
    if 'bid' in fields: output += f"Bid: {data.pop('bid')}\n"
    if 'ask' in fields: output += f"Ask: {data.pop('ask')}\n"
    if 'regularMarketOpen' in fields: output += f"Open: {data.pop('regularMarketOpen')}\n"
    if 'regularMarketPreviousClose' in fields: output += (f"PreviousClose: " +
                                                     f"{data.pop('regularMarketPreviousClose')}\n")
    if 'regularMarketDayHigh' in fields: output += f"DayHigh: {data.pop('regularMarketDayHigh')}\n"
    if 'regularMarketDayLow' in fields: output += f"DayLow: {data.pop('regularMarketDayLow')}\n"
    if 'trailingPE' in fields: output += f"PriceEarnings: {data.pop('trailingPE')}\n"
    if 'marketCap' in fields: output += f"MarketCap: {data.pop('marketCap')}\n"
    if 'volume' in fields: output += f"Volume: {data.pop('volume')}\n"
    output += "  ----  \n"
    # Everything Else
    for k, v in sorted(data.items()):
        if k in ignore: continue
        if v:
            if k[0:7] == 'regular': continue
            output += f"{k[0].upper()}{k[1:]}: {v}\n"
    # Output
    print(output)
    if report:
        with open(f"{CWD}/Quote_{symbol}_" + 
                    f"{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt", 'w') as f:
            f.write("SIMPLE C-LI QUOTER\n\n")
            f.write(f"Report generated: {dt.now().strftime('%H:%M:%S %d-%m-%Y')}\n")
            f.write("_" * 37 + "\n\n")
            f.write(output)
            f.write("\n -- End of report.\n\n")
            f.write("Thank you for using the Simple C-Li Quoter!\n")
        
def main():
    argList = sys.argv[1:]
    opts = "hs:e:rq:"; longOpts = ["help", "symbol=", "exchange=", "report", "query="]
    try:
        args, vals = getopt.getopt(argList, opts, longOpts)
        initiator = ["", "", False, ""]
        for a, v in args:
            if a in ("-h", "--help"): help()
            elif a in ("-s", "--symbol"): initiator[0] = v
            elif a in ("-e", "--exchange"): initiator[1] = v
            elif a in ("-r", "--report"): initiator[2] = True
            elif a in ("-q", "--query"): initiator[3] = v
        if not initiator[0]: raise getopt.error("Usage error.")
    except getopt.error:
        print("Incorrect usage!")
        help()
    quote(*initiator)
    print("Thank you for using the Simple C-Li Quoter!")

def help():
    print("Usage: ./simple_cli_quoter.py [-h] [-s SYMBOL] [-e EXCHANGE] [-r]")
    print("  no arguments:  Display this help message.")
    print("  -e EXCHANGE, --exchange EXCHANGE:  Exchange or Market (eg. ASX, HKEX). " +
                "For currencies, include as 'global'. If omitted this will default to US Markets.")
    print("  -s SYMBOL, --symbol SYMBOL:  Ticker symbol (mandatory).")
    print("  -q FIELD, --query FIELD:  Query for a singular field from the data (no spaces). " +
                "No report will be generated with this option. If the field is not found, " +
                "then the entire data will be output.")
    print("  -h, --help:  Show this help message.")
    print("  -r, --report:  Create a .txt report in the current working directory.")
    print("Argument values are case-insensitive.\nSee the README.md for further details...")
    sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)
