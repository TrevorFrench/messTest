# Messari On-Chain Data Challenge

## :writing_hand: Author

Trevor French <https://trevorfrench.com>

## Functions: 

get_balances, get_token_balance, fetch_all_transactions

### get_balances(addressList)
- addressList: a list of public ethereum addresses
```python
#SET ADDRESS FILE
addressFile = open('addresses.json')
addresses = json.load(addressFile)

#GET DATAFRAME OF WALLETS WITH CURRENT ETH BALANCES
df = get_balances(addresses)
print(df)
```

### get_token_balance(addressList, contractAddress, minABI)
- addressList: a list of public ethereum addresses
- contractAddress: address of desired contract you wish to query
- minABI: the ABI file of the specified contract containing at least the 'balanceOf' method
```python
#SET ABI FILE
abiFile = open('minABI.json')
minABI = json.load(abiFile)

#SET ADDRESS FILE
addressFile = open('addresses.json')
addresses = json.load(addressFile)

#SET CONTRACT ADDRESS (ENS IN THIS CASE)
ensAddress = '0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72'

#GET DATAFRAME OF WALLETS WITH CURRENT ENS BALANCES
df = get_token_balance(addresses, ensAddress, minABI)
print(df)
```

### fetch_all_transactions(beg, end, addressList)
- beg: first block to begin searching
- end: last block to search
- addressList: a list of public ethereum addresses
```python
#SET ADDRESS FILE
addressFile = open('addresses.json')
addresses = json.load(addressFile)

#GET DATAFRAME OF ALL TRANSACTIONS BETWEEN BLOCK 14218907 &
#14218908 WHERE AN ADDRESS IN THE ADDRESS LIST IS ON EITHER 
#SIDE OF THE TRANSACTION
df = fetch_all_transactions(14218907, 14218908, addresses)
print(df)
```