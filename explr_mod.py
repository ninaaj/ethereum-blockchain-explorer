"""
    This file is a python module that utilizes Ethereum's web3 Python API
"""

import time

from web3 import Web3

global web3

web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/10ade1a7a5b04d1db1b50d8a1fe7343b')) 

def check(depth, start):   
    global web3
    
    latest = web3.eth.blockNumber
    
    if latest < start or start < 0:
        print('invalid start block entered')
        return False
    
    if depth > start or depth < 1:
        print('invalid depth entered')
        return False
    
    return True

def get_latest_blocks(depth):
    global web3
    
    latest = web3.eth.blockNumber
    
    if not check(depth,latest):
        return
    
    current_time = time.time() 
    
    for i in range(latest, latest-depth, -1):
        block = web3.eth.getBlock(i)
        if block is None:
            continue
        block_time = round(current_time - block['timestamp'], 2)
        gas_percentage = round((block['gasUsed'] / block['gasLimit']) * 100, 2)
        print(f"-----------------------\nheight:\t\t{i}\nage:\t\t{block_time} seconds\ntransactions:\t{len(block['transactions'])}\nuncles:\t\t{len(block['uncles'])}\nminer:\t\t{block['miner']}\ngas used:\t{block['gasUsed']} ({gas_percentage}%)\ngas limit:\t{block['gasLimit']}")

def get_latest_transactions(depth):
    global web3
    
    latest = web3.eth.blockNumber
    
    if depth < 1:
        print('invalid depth entered')
        return
    
    current_time = time.time() 
    
    tx_counter = 0
    
    for i in range(latest, 0, -1):
        block = web3.eth.getBlock(i,True)
        if block is None:
            continue
        block_time = round(current_time - block['timestamp'], 2)
        for transaction in block['transactions']:
            if tx_counter == depth:
                return
            tx_counter += 1
            print(f"-----------------------\nhash:\t\t{transaction['hash']}\nblock:\t\t{i}\nage:\t\t{block_time} seconds\nto:\t\t{transaction['to']}\nfrom:\t\t{transaction['from']}\ngas:\t\t{transaction['gas']}\ngas price:\t{transaction['gasPrice']}\nvalue:\t\t{transaction['value']}\n")

def get_miner_query(miner, depth, start=False):
    global web3
    
    if not start:
        start = web3.eth.blockNumber
    
    if not check(depth,start):
        return
    
    print('\nthis might take a while')
    
    blocks = get_blocks(miner,depth,start) 
    
    if len(blocks) == 0:
        print(f'\nno blocks found for {miner}\n')
        return
    
    current_time = time.time() 
    
    for block in blocks:
        block_time = round(current_time - block['timestamp'], 2)
        gas_percentage = round((block['gasUsed'] / block['gasLimit']) * 100, 2)
        print(f"-----------------------\nheight:\t\t{block['number']}\nage:\t\t{block_time} seconds\ntransactions:\t{len(block['transactions'])}\nuncles:\t\t{len(block['uncles'])}\nminer:\t\t{block['miner']}\ngas used:\t{block['gasUsed']} ({gas_percentage}%)\ngas limit:\t{block['gasLimit']}")
    
    print(f'\n{len(blocks)} block(s) found for miner {miner}\n')

def get_blocks(miner, depth, start):   
    global web3
    
    blocks = []
    
    for i in range(start, start-depth, -1):
        block = web3.eth.getBlock(i)
        if block is not None and block['miner'] == miner:
            blocks.append(block)   
    return blocks
 

def get_transaction_query(depth,to=False,fr=False,start=False):
    global web3
    
    if not to and not fr:
        print('must give TO and/or FROM address')
        return
    
    if not start:
        start = web3.eth.blockNumber
    
    if not check(depth,start):
        return

    print('\nthis might take a while')
    
    transactions = []
    
    if to and fr:
        transactions = tf_tx_helper(to,fr,depth,start)
    elif to:
        transactions = to_tx_helper(to,depth,start)
    else:
        transactions = from_tx_helper(fr,depth,start)
    
    if len(transactions) == 0:
        print('\nno transactions found\n')
        return
    
    current_time = time.time() 
    current_block, block_time = -1, 0
    for transaction in transactions:
        if current_block != transaction['blockNumber']:
            block = web3.eth.getBlock(transaction['blockNumber'])
            block_time = round(current_time - block['timestamp'], 2)
        print(f"-----------------------\nhash:\t\t{transaction['hash']}\nblock:\t\t{transaction['blockNumber']}\nage:\t\t{block_time} seconds\nto:\t\t{transaction['to']}\nfrom:\t\t{transaction['from']}\ngas:\t\t{transaction['gas']}\ngas price:\t{transaction['gasPrice']}\nvalue:\t\t{transaction['value']}\n")
    print(f'\n{len(transactions)} transaction(s) found\n')
    
def tf_tx_helper(to,fr,depth,start):
    global web3
    transactions = [] 
    for i in range(start, start-depth, -1):
        block = web3.eth.getBlock(i,True)
        if block is None:
            continue
        for transaction in block['transactions']:
            if transaction['to'] == to and transaction['from'] == fr:
                transactions.append(transaction)
    return transactions

def to_tx_helper(to,depth,start):
    global web3
    transactions = [] 
    for i in range(start, start-depth, -1):
        block = web3.eth.getBlock(i,True)
        if block is None:
            continue
        for transaction in block['transactions']:
            if transaction['to'] == to:
                transactions.append(transaction)
    return transactions

def from_tx_helper(fr,depth,start):
    global web3
    transactions = [] 
    for i in range(start, start-depth, -1):
        block = web3.eth.getBlock(i,True)
        if block is None:
            continue
        for transaction in block['transactions']:
            if transaction['from'] == fr:
                transactions.append(transaction)
    return transactions
