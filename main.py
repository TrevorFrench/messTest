# TITLE: Messari On-Chain Data Challenge
# DESCRIPTION: Uses web3.py to query ETH balance, ENS balance,
#   as well as transaction history for a given array of public 
#   addresses
# TODO:
# - See if there is a way to scale up transaction fetching
# - Clean-up code
# - Store assets in a sub-folder
# - Get rid of unnecessary 'prints'
# - Make functions able to accept a list of addresses
# - Catch errors if list items don't exist (need a value on every line to preserve order)
# - Parse swaps
# - Might be able to merge each dictionary

#MODULES
from web3 import Web3, HTTPProvider
import json
import pandas as pd

#CONNECT TO NODE
w3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/9675ce340c39409d9cc2d5820ad10796'))

#LOAD FILES
with open('minABI.json') as abiFile:
  minABI = json.load(abiFile)

with open('ensABI.json') as ensAbiFile:
  contractABI = json.load(ensAbiFile)

with open('addresses.json') as addressFile:
  addresses = json.load(addressFile)

ensAddress = '0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72'

test = '0x18aD506fFC6bD1977d94d48466680ADacf366cA4'

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

#GET ENS TOKEN BALANCE
def get_token_balance(addressList, contractAddress, minABI):
  balanceList = []
  for item in addressList:
    token = w3.eth.contract(address=ensAddress, abi=minABI)
    token_balance =  token.functions.balanceOf(item).call()
    balanceList.append(token_balance / 1e18)
  df = pd.DataFrame()
  df['Address'] = addressList
  df['Balance'] = balanceList
  return df

#CHECK ENS DOMAIN AVAILABILITY
def check_available(domain):
  contractAddress = '0x283Af0B28c62C092C9727F1Ee09c02CA627EB7F5'
  contract = w3.eth.contract(address=contractAddress, abi=contractABI)
  function = contract.functions.available(domain).call()
  return function

#GET THE TRANSACTION HISTORY
def fetch_all_transactions(beg, end, addressList):
  blockHashList = []
  fromList = []
  toList = []
  blockNumList = []
  chainIdList = []
  gasList = []
  gasPriceList = []
  txHashList = []
  inputList = []
  typeList = []
  valueList = []
  
  i = beg
  while i <= end:
    block = w3.eth.get_block(i)
    print("Scanning Block: ", i)
    n = 0
    z = len(block.transactions)
    while n < z:
      txhash = block.transactions[n].hex()
      transaction = w3.eth.getTransaction(txhash)
      txfrom = transaction['from']
      txto = transaction['to']
      
      df = pd.DataFrame()
      if txfrom in addressList or txto in addressList:
        blockHashList.append(transaction['blockHash'].hex())
        fromList.append(txfrom)
        toList.append(txto)
        blockNumList.append(transaction['blockNumber'])
        chainIdList.append(transaction['chainId'])
        gasList.append(transaction['gas'])
        gasPriceList.append(transaction['gasPrice'])
        txHashList.append(transaction['hash'].hex())
        inputList.append(transaction['input'])
        typeList.append(transaction['type'])
        valueList.append(transaction['value'])
      n += 1
    i += 1
    
  df = pd.DataFrame()
  df['Block_Hash'] = blockHashList
  df['From'] = fromList
  df['To'] = toList
  df['Block_Number'] = blockNumList
  df['Chain_ID'] = chainIdList
  df['Gas'] = gasList
  df['Gas_Price'] = gasPriceList
  df['Tx_Hash'] = txHashList
  df['Input'] = inputList
  df['Type'] = typeList
  df['Value'] = valueList
  
  return df


#DELETE ME
def test_transactions(block):
  block = w3.eth.get_block(block)
  txhash = block.transactions[0].hex()
  print("txhash: ", txhash)
  transaction = w3.eth.getTransaction(txhash)
  print(transaction)

def test_specific_transactions(address):
  transaction = w3.eth.getTransaction(address)
  print(transaction['input'])
  print(int(transaction['input'], 16))

#test_specific_transactions('0x85207ece73fdfe35e26d213486ff77ae4f4024a67ac3ea9bff655026a42d71bb')

#test_transactions(14218907)
#df = get_balances(addresses)
#print(df)

#df = fetch_all_transactions(14218907, 14218908, addresses)
#print(df)

#df = get_token_balance(addresses, ensAddress, minABI)
#print(df)