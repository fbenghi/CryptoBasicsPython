"""
Script base: https://web3py.readthedocs.io/en/stable/examples.html#working-with-an-erc20-token-contract

Descrição: faz transação, vê saldo
"""

#%%
from web3 import Web3

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
# Contract creation
w3.eth.getTransactionReceipt('0xb9a40a1e49af1026b51044727a12c3e2bf88d6120dbf4e912df100fe732e4342')
# %%
#load ERC contract
contractAddress = '0x26760F09b813C49B731837ab2dF23e3b82f0dfDc'

import json
with open('/home/felipe/Documents/Ethereum/Scripts/Remix-Ide/Contracts/Contracts/artifacts/FucksToken.json') as json_file:
    contractData = json.load(json_file)


contract = w3.eth.contract(contractAddress, abi=contractData["abi"])


"""
Funcoes de interface do contrato
"""
# %%
contract.functions.name().call()
# %%
contract.functions.symbol().call()
# %%
decimals = contract.functions.decimals().call()
# %%
contract.functions.totalSupply().call()


# %%
#atribui um nome aos enderecos
contractOwner = w3.eth.accounts[9]
alice         = w3.eth.accounts[0] 
bob           = w3.eth.accounts[0] 
contract.functions.balanceOf(contractOwner).call()

"""
Funcoes de transferencia de token
"""

# %%
# Transfere diretamente
tx_hash = contract.functions.transfer(bob, 100).transact({'from': contractOwner})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print('Bob', contract.functions.balanceOf(bob).call())
print('ContractOwner', contract.functions.balanceOf(contractOwner).call())

# %%
# Cria permissão de transferência
contract.functions.allowance(contractOwner, bob).call()
tx_hash = contract.functions.approve(bob, 2000).transact({'from': contractOwner})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Bob pode transferir {amount} da conta principal".format(amount=contract.functions.allowance(contractOwner, bob).call()))

# %%
# Transfere os tokens de terceiros
tx_hash = contract.functions.transferFrom(contractOwner, alice, 75).transact({'from': bob})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print('Alice', contract.functions.balanceOf(alice).call())


#%%%
"""
Lendo eventos do blockchain
"""

#%%%
# busca por um evento específico
contract.events.Transfer().processReceipt(tx_receipt)

# %%
transfer_filter = contract.events.Transfer.createFilter(fromBlock="0x0", argument_filters={'from': contractOwner})
transfer_filter.get_new_entries()

# %%
#tx1
tx_hash = contract.functions.transferFrom(contractOwner, alice, 75).transact({'from': bob})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)


#tx2
tx_hash = contract.functions.transferFrom(contractOwner, alice, 75).transact({'from': bob})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)


#tx3
tx_hash = contract.functions.transferFrom(contractOwner, alice, 75).transact({'from': bob})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)


# Get the event from all new transfers
newTransfers = transfer_filter.get_new_entries()
newTransfers
# %%
