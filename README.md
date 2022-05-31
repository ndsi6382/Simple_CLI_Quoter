# Simple C-Li Quoter

This is a simple command line program to retrieve and display financial data 
from Yahoo Finance.

## Setup
There is only one dependency: `yfinance`, which can be installed with:
`pip install yfinance`.  
After navigating to the directory of the program, run 
`sudo chmod +x ./simple_cli_quoter.py` to allow the file's execution.

## Usage
Usage is as follows: 
`./simple_invoice_generator.py [-h] [-s SYMBOL] [-e EXCHANGE] [-r]`.  
If no arguments are given, the help message is displayed.
- `-s SYMBOL` sets the ticker symbol for lookup. This is a mandatory argument.
- `-e EXCHANGE` sets the exchange or market for the symbol (eg. ASX, HKEX...).
For currencies, set it as 'global'. If omitted for stock exchange symbols, 
this will default to US markets.
- `-r REPORT` optionally allows for a .txt report to be created in the current 
working directory.
- `-q FIELD` optionally allows for the querying of a singular field from the 
data (with no spaces). A report will never be generated with this option, and 
if the field is not found, then the entire data will be output.
- `-h` displays the help message.  

Note the following additional points:
- Arguments are case-insensitive.
- Currency pair symbols are concatenations of their symbols: USD and AUD = 
`USDAUD`.
- Most US and Japanese stocks do not need to be explicitly set an exchange.
- Cryptocurrencies mostly only exist as pairs with USD (apart from some 
blue-chips such as Bitcoin and Ethereum). No exchange needs to be declared for 
these, but their symbols are concatenations of their symbols, joined by a 
hyphen: ETH and USD = `ETH-USD`.
