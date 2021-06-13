# #%%
# from web3 import Web3

# import json
# with open('/home/felipe/Documents/Ethereum/Scripts/Remix-Ide/Contracts/Contracts/artifacts/FucksToken.json') as json_file:
#     contractData = json.load(json_file)

# w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# deploy_address = w3.eth.accounts[0] 

# abi = contractData["abi"]

# bytecode = contractData["data"]["bytecode"]["object"]

# # Create our contract class.
# Erc20Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
# # issue a transaction to deploy the contract.
# tx_hash = Erc20Contract.constructor().transact({
#     'from': deploy_address,
# })
# # wait for the transaction to be mined
# tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, 180)
# # instantiate and return an instance of our contract.



import pytest

from web3 import (
    EthereumTesterProvider,
    Web3,
)

import json


with open('/home/felipe/Documents/Ethereum/Scripts/Remix-Ide/Contracts/artifacts/FucksToken.json') as json_file:
    contractData = json.load(json_file)



@pytest.fixture
def tester_provider():
    return EthereumTesterProvider()


@pytest.fixture
def eth_tester(tester_provider):
    return tester_provider.ethereum_tester


@pytest.fixture
def w3(tester_provider):
    return Web3(tester_provider)


@pytest.fixture
def erc20_contract(eth_tester, w3):

    deploy_address = eth_tester.get_accounts()[0]

    abi = contractData["abi"]

    bytecode = contractData["data"]["bytecode"]["object"]

    # Create our contract class.
    Erc20Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    # issue a transaction to deploy the contract.
    tx_hash = Erc20Contract.constructor().transact({
        'from': deploy_address,
    })
    # wait for the transaction to be mined
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, 180)
    # instantiate and return an instance of our contract.
    return Erc20Contract(tx_receipt.contractAddress)


def test_initial_greeting(erc20_contract):
    """
    Unit test de função que não modifica o estado do blockchain
    """
    hw = erc20_contract.caller.symbol()
    assert hw == '0FUCKS'

def test_transaction(erc20_contract, eth_tester, w3):
    """
    Unit test de transação de token
    """

    #determina quais são as contas usadas
    contractOwner = eth_tester.get_accounts()[0]
    tokenReceiver = eth_tester.get_accounts()[1]

    #armazena o estado inicial
    amountInitOwner    = erc20_contract.caller.balanceOf(contractOwner)
    amountInitReceiver = erc20_contract.caller.balanceOf(tokenReceiver)
    amountTx = 100

    #faz a transferencia de tokens  
    tx_hash = erc20_contract.functions.transfer(tokenReceiver, amountTx).transact({'from': contractOwner})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash, 180)  
    
    #armazena o estado final
    amountRx = erc20_contract.caller.balanceOf(tokenReceiver)
    amountFinalOwner    = erc20_contract.caller.balanceOf(contractOwner)
    amountFinalReceiver = erc20_contract.caller.balanceOf(tokenReceiver)


    #garante que houve mudança de saldo    
    assert amountFinalOwner    == (amountInitOwner-amountTx)
    assert amountFinalReceiver == (amountInitReceiver+amountTx)

    #garante que o evento está certo
    logs = erc20_contract.events.Transfer.getLogs()
    assert len(logs) == 1
    event = logs[0]
    assert event.blockHash == receipt.blockHash
    assert event.args.tokens == amountTx
