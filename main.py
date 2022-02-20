# TITLE: Messari On-Chain Data Challenge
# DESCRIPTION: Uses web3.py to query ETH balance, ENS balance,
#   transaction history for a given array of public addresses,
#   as well as the availability of any specified ENS domain
# TODO:
# - Figure out how to parse swaps. Do you need to include ABI for each DeFi platform?
# - 
# -

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

#GET CURRENT ETH BALANCES
def get_balances(addressList):

  try:
    balanceList = []
  
    #Queries eth balance for each address and adds the balance to a list
    for item in addressList:
      balance = w3.eth.get_balance(item)
      balanceList.append(balance / 1e18)
  
    #Creates a dataframe with addresses and their respective balances
    df = pd.DataFrame()
    df['Address'] = addressList
    df['Balance'] = balanceList
    
    return df
    
  except:
    print('An error occurred retrieving ETH balances. Please check your inputs and try again.')
    return

#GET ENS TOKEN BALANCE
def get_token_balance(addressList, contractAddress, minABI):
  
  try:
    balanceList = []
    
    #Queries ens balance for each address and adds the balance to a list
    for item in addressList:
      token = w3.eth.contract(address=ensAddress, abi=minABI)
      token_balance =  token.functions.balanceOf(item).call()
      balanceList.append(token_balance / 1e18)
  
    #Creates a dataframe with addresses and their respective balances
    df = pd.DataFrame()
    df['Address'] = addressList
    df['Balance'] = balanceList
    
    return df
    
  except:
    print('An error occurred retrieving ENS balances. Please check your inputs and try again.')
    return

#CHECK ENS DOMAIN AVAILABILITY
def check_available(domain):
  
  try:
    #Leverages the 'available' function on the ENS smart contract
    contractAddress = '0x283Af0B28c62C092C9727F1Ee09c02CA627EB7F5'
    contract = w3.eth.contract(address=contractAddress, abi=contractABI)
    function = contract.functions.available(domain).call()
    return function
    
  except:
    print('An error occurred while verifying availability. Please check your inputs and try again.')
    return

#GET THE TRANSACTION HISTORY
def fetch_all_transactions(beg, end, addressList):

  try:

    #Initialize lists
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

    #Outer Loop: Gets each block in the specified range
    i = beg
    while i <= end:
      
      block = w3.eth.get_block(i)
      print("Scanning Block: ", i)
      n = 0
      z = len(block.transactions)

      #Inner Loop: Checks each transaction in the block
      while n < z:
        
        txhash = block.transactions[n].hex()
        transaction = w3.eth.getTransaction(txhash)
        txfrom = transaction['from']
        txto = transaction['to']

        #If an address in the input array is associated with the transaction, log the transaction details
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

    #Create dataframe  
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
    
  except:
    print('An error occurred retrieving transaction history. Please check your inputs and try again. If error persists, try narrowing your block search. @dev: persistent errors may require parsing values dynamically.')
    return