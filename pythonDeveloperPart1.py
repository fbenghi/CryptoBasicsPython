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
w3 = Web3(Web3.EthereumTesterProvider())

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
