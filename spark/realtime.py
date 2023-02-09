from array import ArrayType
from pyspark.sql.functions import *
from pyspark.sql.types import *
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
from pyspark.sql import SparkSession

schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("volume", DoubleType(), True),
    StructField("cp", DoubleType(), True),
    StructField("rcp", DoubleType(), True),
    StructField("a", DoubleType(), True),
    StructField("ba", DoubleType(), True),
    StructField("sa", DoubleType(), True),
    StructField("hl", DoubleType(), True),
    StructField("pcp", DoubleType(), True),
    StructField("time", StringType(), True),
])
spark = SparkSession.builder\
    .config("spak.app.name", "StreamStock")\
    .config("spark.master", "local[*]")\
    .config("spark.jars","./spark/src/elasticsearch-hadoop-7.15.1.jar")\
    .config("spark.driver.extraClassPath","./spark/src/elasticsearch-hadoop-7.15.1.jar")\
    .config("spark.es.nodes", "localhost")\
    .config("spark.es.port", "9200")\
    .config("spark.es.nodes.wan.only", "false")\
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")
es = Elasticsearch(hosts='http://localhost:9200')

consumer = KafkaConsumer(
        'realtimeStockData',
        bootstrap_servers=['localhost:19092','localhost:29092', 'localhost:39092'],
        group_id='realtimeStockDataConsummers',
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
print("asd")
for event in consumer:
    event_data = event.value
    df = spark.createDataFrame([event_data], schema)
    df.show(1)
    es.update(index="stocks", id=f"{df.first().symbol}_{df.first().time}", doc=json.loads(json.dumps(event_data)), doc_as_upsert=True)
    
    