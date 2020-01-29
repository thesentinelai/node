from web3 import Web3,HTTPProvider

w3 = Web3(HTTPProvider('https://testnet2.matic.network'))

print(w3.isConnected())
