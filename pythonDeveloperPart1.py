"""
Script base: https://ethereum.org/en/developers/tutorials/a-developers-guide-to-ethereum-part-one/

Descrição: faz transação, vê saldo
"""

#%%
from web3 import Web3

# %%
Web3.toWei(1, 'ether')

# %%
Web3.fromWei(1, 'gwei')

# %%
# conectando no nó fake
# w3 = Web3(Web3.EthereumTesterProvider())
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# %%
# Verificando conexão
w3.isConnected()

# %%
# Contas pre-adicionadas
w3.eth.accounts


# %%
# Saldo da conta
weiValue = w3.eth.getBalance(w3.eth.accounts[0])
Web3.fromWei(weiValue, 'ether')

# %%
# Ultimo bloco
w3.eth.getBlock('latest')

# %%
# Transacao
tx_hash = w3.eth.sendTransaction({
   'from': w3.eth.accounts[0],
   'to': w3.eth.accounts[1],
   'value': w3.toWei(3, 'ether')
})
tx_hash

# %%
# Aguarda inclusao da transacao no bloco
w3.eth.waitForTransactionReceipt(tx_hash)

#%%
Web3.fromWei(w3.eth.getBalance(w3.eth.accounts[0]), 'ether')
# %%
Web3.fromWei(w3.eth.getBalance(w3.eth.accounts[1]), 'ether')
# %%
# Contract interaction
w3.eth.getTransactionReceipt('0x2c35813d4ec6aa1f346008273489c6ecefbbddeceb8ec19b364c6b2a7cf415e6')

# %%
# Contract creation
w3.eth.getTransactionReceipt('0xb9a40a1e49af1026b51044727a12c3e2bf88d6120dbf4e912df100fe732e4342')
# %%
#load ERC contract
contractAddress = '0x26760F09b813C49B731837ab2dF23e3b82f0dfDc'

import json
with open('/home/felipe/Documents/Ethereum/Scripts/Remix-Ide/Contracts/Contracts/artifacts/FucksToken.json') as json_file:
    contractData = json.load(json_file)


contract = w3.eth.contract(contractAddress, abi=contractData["abi"])

# %%
contract.functions.name().call()
# %%
contract.functions.symbol().call()
# %%
decimals = contract.functions.decimals().call()
# %%
contract.functions.totalSupply().call()
# %%
contractOwner = w3.eth.accounts[9]
contract.functions.balanceOf(contractOwner).call()
# %%
