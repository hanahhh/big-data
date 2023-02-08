from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    date_trunc, col, split, decode
)
from elasticsearch import Elasticsearch


from pyspark.sql.types import *
from pandas import json_normalize
spark = SparkSession.builder\
    .config("spak.app.name", "StreamStock")\
    .config("spark.master", "local[*]")\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1")\
    .enableHiveSupport()\
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

es = Elasticsearch(hosts='http://es-container:9200')


df = spark.readStream.format('kafka')\
    .option('kafka.bootstrap.servers', 'localhost:19092,localhost:29092,localhost:39092')\
    .option('subscribe', 'realtimeStockData')\
    .config("spark.es.nodes", "elasticsearch")\
    .config("spark.es.port", "9200")\
    .config("spark.es.nodes.wan.only", "false")\
    .load()
df.printSchema()
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
# df.writeStream.start().awaitTermination()
# df.show(5)

# print(df.value)
df = df.select(decode(col('value'), 'UTF-8').alias('value'),
               col('timestamp').alias('recorded_time'))

df = df.withColumn('symbol', (split(col('value'), ',').getItem(0)))
df = df.withColumn('volume', (split(col('value'), ',').getItem(1)))
df = df.withColumn('cp', (split(col('value'), ',').getItem(2)))
df = df.withColumn('rcp', (split(col('value'), ',').getItem(3)))
df = df.withColumn('a', (split(col('value'), ',').getItem(4)))
df = df.withColumn('ba', (split(col('value'), ',').getItem(5)))
df = df.withColumn('sa', (split(col('value'), ',').getItem(6)))
df = df.withColumn('hl', (split(col('value'), ',').getItem(7)))
df = df.withColumn('pcp', (split(col('value'), ',').getItem(8)))
df = df.withColumn('time', (split(col('value'), ',').getItem(9)))

# df = df.select(from_json('value', schema).alias('json'))
df.writeStream.foreachBatch(save_els).format('console').outputMode(
    "append").start().awaitTermination()


def save_els(df):
    es.update(index="stock", id=1, doc=df,  doc_as_upsert=True)
