from cassandra.cluster import Cluster

cluster = Cluster(['172.18.0.12'])
session = cluster.connect()

# session.execute("CREATE KEYSPACE coinhub\
#     WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3}")

session.execute("USE coinhub")

session.execute("CREATE TABLE coin_data (\
   symbol text,\
   recorded_time timestamp,\
   frequency text,\
   high double,\
   low double,\
   open double,\
   close double,\
   volume double,\
   PRIMARY KEY (symbol, recorded_time)\
) WITH CLUSTERING ORDER BY (recorded_time DESC)")

session.execute("CREATE TABLE tweet_trending (\
   symbol text,\
   recorded_time timestamp,\
   frequency text,\
   count int,\
   sentiment int,\
   PRIMARY KEY (symbol, recorded_time)\
) WITH CLUSTERING ORDER BY (recorded_time DESC)")

session.execute("CREATE TABLE stream_tweet_trending (\
   symbol text,\
   recorded_time timestamp,\
   frequency text,\
   count int,\
   sentiment int,\
   PRIMARY KEY (symbol, recorded_time)\
) WITH CLUSTERING ORDER BY (recorded_time DESC)")

session.execute("CREATE TABLE recent_tweet (\
   symbol text,\
   recorded_time timestamp,\
   content text,\
   PRIMARY KEY (symbol, recorded_time)\
) WITH CLUSTERING ORDER BY (recorded_time DESC)")

session.shutdown()
