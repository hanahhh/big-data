from cassandra.cluster import Cluster

cluster = Cluster(['172.20.0.11'])
session = cluster.connect()

# session.execute("CREATE KEYSPACE stock\
#     WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1}")

session.execute("USE stock")

session.execute("CREATE TABLE stock_data (\
   symbol text,\
   high double,\
   low double,\
   open double,\
   close double,\
   volume double,\
   trading_date timestamp,\
   PRIMARY KEY (symbol, trading_date)\
) WITH CLUSTERING ORDER BY (trading_date DESC)")

session.execute("CREATE TABLE predicted_price (\
   symbol text,\
   high double,\
   low double,\
   open double,\
   close double,\
   PRIMARY KEY (symbol)\
)")

# session.execute("CREATE TABLE tweet_trending (\
#    symbol text,\
#    recorded_time timestamp,\
#    frequency text,\
#    count int,\
#    sentiment int,\
#    PRIMARY KEY (symbol, recorded_time)\
# ) WITH CLUSTERING ORDER BY (recorded_time DESC)")

# session.execute("CREATE TABLE stream_tweet_trending (\
#    symbol text,\
#    recorded_time timestamp,\
#    frequency text,\
#    count int,\
#    sentiment int,\
#    PRIMARY KEY (symbol, recorded_time)\
# ) WITH CLUSTERING ORDER BY (recorded_time DESC)")

# session.execute("CREATE TABLE recent_tweet (\
#    symbol text,\
#    recorded_time timestamp,\
#    content text,\
#    PRIMARY KEY (symbol, recorded_time)\
# ) WITH CLUSTERING ORDER BY (recorded_time DESC)")

session.shutdown()
