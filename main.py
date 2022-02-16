# TITLE: Messari On-Chain Data Challenge
# DESCRIPTION: Uses web3.py to query ETH balance, ENS balance,
#   as well as transaction history for a given array of public 
#   addresses
# TODO:
# - See if there is a way to scale up transaction fetching
# - Output results into dataframes
# - Create array of public addresses
# - Clean-up code
# - Store assets in a sub-folder
# - Get rid of unnecessary 'prints'
# - Make functions able to accept a list of addresses
# - Change append to concat

#MODULES
from web3 import Web3, HTTPProvider
import json
import pandas as pd

#CONNECT TO NODE
w3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/9675ce340c39409d9cc2d5820ad10796'))

#LOAD FILES
abiFile = open('minABI.json')
minABI = json.load(abiFile)

addressFile = open('addresses.json')
addresses = json.load(addressFile)

#GET CURRENT ETH BALANCES
def get_balances(addressList):
  balanceList = []
  for item in addressList:
    balance = w3.eth.get_balance(item)
    balanceList.append(balance / 1e18)
  df = pd.DataFrame()
  df['Address'] = addressList
  df['Balance'] = balanceList
  return df

#df = get_balances(addresses)
#print(df)

#GET ENS TOKEN BALANCE
ensAddress = '0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72'
token = w3.eth.contract(address=ensAddress, abi=minABI) # declaring the token contract
token_balance = token.functions.balanceOf('0x18aD506fFC6bD1977d94d48466680ADacf366cA4').call() # returns int with balance, without decimals
print("ENS BALANCE: ", token_balance / 1e18)

#GET THE TRANSACTION HISTORY
def fetch_all_transactions(beg, end, address):
  i = beg
  while i <= end:
    block = w3.eth.get_block(i)
    print("Length: ", len(block.transactions))
    n = 0
    z = len(block.transactions)
    while n < z:
      txhash = block.transactions[n].hex()
      transaction = w3.eth.getTransaction(txhash)
      txfrom = transaction['from']
      txto = transaction['to']
      if address == txfrom:
        print("txhash from: (", n + 1, "/", z, ") ", txhash)
      elif address == txto:
        print("txhash to: (", n + 1, "/", z, ") ", txhash)
      n += 1
    i += 1

#fetch_all_transactions(14218907, 14218908, "0x8817D887960737A604Cf712d3E5da8673DDdb7F0")

def test_transactions(block):
  block = w3.eth.get_block(block)
  txhash = block.transactions[0].hex()
  print("txhash: ", txhash)

  transaction = w3.eth.getTransaction(txhash)
  print("Transaction From: ", transaction['from'])
  print("Transaction To: ", transaction['to'])

#test_transactions(14218907)