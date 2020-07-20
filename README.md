# Anomaly Detection in Bitcoin Transaction Network
This project explores some basic anomaly detection techniques in the Bitcoin transaction network. Please look at the article in this link to find more information: (ADD MEDIUM ARTICLE LINK)

## Creating the Bitcoin Transaction Network
The Bitcoin dataset used in this project can be found in https://senseable2015-6.mit.edu/bitcoin/. To make the network using this data, follow this repo: https://github.com/dkondor/txedges. After processing the Bitcoin data, the network dataset used in this project can be found in txedges.dat in pp-data. The data is tab separated list of edges having 4 columns: transaction id, transaction input address id, transaction output address id, weight. Hence, addresses act as nodes with transactions as directed edges weighted by transaction id's and transaction weights(in satoshis).

## Contributors:
- Kavita Vaishnaw (https://github.com/kavita-v)
- Kanishk Kalra (https://github.com/kanishkkalra11)
- Mohit Mina
