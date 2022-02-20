# Messari On-Chain Data Challenge
This program allows the user to do the following:
- Retrieve current balance of a given list of public Ethereum addresses
- Retrieve current ENS balance of a given list of public Ethereum addresses
- Retrieve transaction history of a given list of public ethereum addresses
- Check the availability of any given ENS domain name

## :page_facing_up: Instructions
1. Navigate to Replit: <https://replit.com/@TrevorFrench/messTest>
2. Press "run" so the functions are accessible from the console
3. Type "get_balances(addresses)" in the console to print a dataframe containing the public addresses along with the current ETH balance of each address listed in the "addresses.json" file.
4. Type "get_token_balance(addresses, ensAddress, minABI)" in the console to print a dataframe containing public addresses and ENS balance for each address in the JSON file.
5. Type "fetch_all_transactions(14218907, 14218908, addresses)" in the console to return all transactions in blocks 14218907 through 14218908 where an address in the list was on either side of the transaction.
6. Type "check_available('trevorfrench')" into the console to see if 'trevorfrench.eth' is an available ENS domain name.

## :writing_hand: Author

Trevor French <https://trevorfrench.com>

## Functions: 

get_balances, get_token_balance, fetch_all_transactions, check_available

### get_balances(addressList)
- addressList: a list of public ethereum addresses
```python
#SET ADDRESS FILE
with open('addresses.json') as addressFile:
  addresses = json.load(addressFile)

#GET DATAFRAME OF WALLETS WITH CURRENT ETH BALANCES
get_balances(addresses)
```

### get_token_balance(addressList, contractAddress, minABI)
- addressList: a list of public ethereum addresses
- contractAddress: address of desired contract you wish to query
- minABI: the ABI file of the specified contract containing at least the 'balanceOf' method
```python
#SET ABI FILE
with open('minABI.json') as abiFile:
  minABI = json.load(abiFile)

#SET ADDRESS FILE
with open('addresses.json') as addressFile:
  addresses = json.load(addressFile)

#SET CONTRACT ADDRESS (ENS IN THIS CASE)
ensAddress = '0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72'

#GET DATAFRAME OF WALLETS WITH CURRENT ENS BALANCES
get_token_balance(addresses, ensAddress, minABI)
```

### fetch_all_transactions(beg, end, addressList)
- beg: first block to begin searching
- end: last block to search
- addressList: a list of public ethereum addresses
```python
#SET ADDRESS FILE
with open('addresses.json') as addressFile:
  addresses = json.load(addressFile)

#GET DATAFRAME OF ALL TRANSACTIONS BETWEEN BLOCK 14218907 &
#14218908 WHERE AN ADDRESS IN THE ADDRESS LIST IS ON EITHER 
#SIDE OF THE TRANSACTION
fetch_all_transactions(14218907, 14218908, addresses)
```

### check_available(domain)
- domain: a string containing the domain name you wish to check the availability of
```python
#SET ABI FILE
with open('ensABI.json') as ensAbiFile:
  contractABI = json.load(ensAbiFile)

#CHECK IF A GIVEN DOMAIN IS AVAILABLE
check_available('trevorfrench') #Returns 'False'
```