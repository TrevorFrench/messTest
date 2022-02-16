# TITLE: Messari On-Chain Data Challenge
# DESCRIPTION: Uses web3.py to accomplish several tasks
# TODO:
# -
# -
# -

#MODULES
from web3 import Web3, HTTPProvider

#CONNECT TO NODE
w3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/9675ce340c39409d9cc2d5820ad10796'))

#PRINT CURRENT BLOCK NUMBER
print ("Latest Ethereum block number" , w3.eth.blockNumber)

#GET CURRENT ETH BALANCE
balance = w3.eth.get_balance('0x18aD506fFC6bD1977d94d48466680ADacf366cA4')
print("Current Balance: ", balance / 1e18)

#GET ENS TOKEN BALANCE

minABI = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
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
      print("txhash: (", n + 1, "/", z, ") ", txhash)
      n += 1
    i += 1

fetch_all_transactions(14218907, 14218908, "x")
#block = w3.eth.get_block(14218907)
#txhash = block.transactions[0].hex()
#print("txhash: ", txhash)

#transaction = w3.eth.getTransaction(txhash)
#print("Transaction: ", transaction)