from cassandra.cluster import Cluster

cluster = Cluster(['172.23.0.11'])
session = cluster.connect()

# session.execute("CREATE KEYSPACE stock\
#     WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3}")

session.execute("USE stock")

# session.execute("CREATE TABLE stock_data (\
#    symbol text,\
#    high double,\
#    low double,\
#    open double,\
#    close double,\
#    volume double,\
#    trading_date timestamp,\
#    PRIMARY KEY (symbol, trading_date)\
# ) WITH CLUSTERING ORDER BY (trading_date DESC)")

# session.execute("CREATE TABLE predicted_price (\
#    symbol text,\
#    high double,\
#    low double,\
#    open double,\
#    close double,\
#    PRIMARY KEY (symbol)\
# )")

session.execute("INSERT INTO stock_data(symbol, trading_date, open, close, high, low, volume) VALUES ('VVS', '2022-10-07', 18000.0, 20000.0, 20300.0, 18000.0, 12100.0)")

session.shutdown()