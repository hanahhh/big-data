from pyspark.sql import SparkSession
from pyspark.sql.functions import date_trunc, from_unixtime, col, max, min, sum, first, last, lit


# replace host cassandra !!! 
spark = SparkSession.builder\
            .config("spark.app.name", "CoinTradeDataAnalyzer")\
            .config("spark.master", "spark://spark-master:7077")\
            .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0")\
            .config("spark.cassandra.connection.host", "172.18.0.12")\
            .config("spark.cassandra.auth.username", "cassandra")\
            .config("spark.cassandra.auth.password", "cassandra")\
            .enableHiveSupport()\
            .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

frequency = ['minute', 'hour', 'day', 'week', 'month', 'year']
def map_time(df, frequency):
    return df.withColumn('Trade time', date_trunc(
        frequency, from_unixtime(col('Trade time') / 1000)))

# print("cassandra", result_df.head(10))
# hdfs: path to folder data
# ex: hdfs://namenode:9000/coinTradeData/2023/1/26/coinTradeData.1674733636
df = spark.read.format('csv')\
    .option('header', True)\
    .option('inferSchema', True)\
    .load("hdfs://namenode:9000/coinTradeData/2023/1/26/")
print(df.head(10))

# print("success", df.count())

# save data into cassandra
# df.write.format('org.apache.spark.sql.cassandra')\
#         .mode('append')\
#         .options(table='coin_data', keyspace='coinhub')\
#         .save()

# print(df.show(3))
# read data from cassandra
# result_df = spark.read.format('org.apache.spark.sql.cassandra')\
#             .options(table='coin_data', keyspace='coinhub')\
#             .load()
