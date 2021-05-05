
<img src="images/miner_stats.png" style="margin: 0px 20%;"></img>

This repository gets the scraped data from www.blockchain. which contains the information of the historical mined block.

## Start Scrapping

Run init_scraping.ipynb, but before make sure the names of HTML classes from www.blockchain.com is not changed it

to modify the HTML Clases, inspect those elements

    class html_class:
        
        height_link = HTML CLASS HEIGH NUMBER
        div_table = HTML CLASS OF ALL TABLE
        left_column_table = HTML CLASS LEFT COLUMN
        right_column_table = HTML CLASS RIGHT COLUMN
        miner_name = MINER NAME RIGHT COLUMN

- - - 
## Miners rewards history Dataset

**Miner Rewards History per day.**

- Hash: Hash Founded for and will use it to the next block
- Confirmations: Confirmations by other nodes
- Timestamp
- Height: BLock ID, first block is 1 
- Number of Transactions
- Difficulty: Difficulty for find the hash
- Merkle root
- Version
- Bits
- Size: Memory use for each block
- Nonce: random number 32-bits
- Transaction Volume
- Block Reward: Actual Block Reward
- Fee Reward
- Miner Name: Company or pool who found the hash
- URl Miner: addres miner link
