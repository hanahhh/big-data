import os
import logging
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    date_trunc, col,
    udf, count, sum, lit, split, decode, length, translate
)
from pyspark.sql.types import IntegerType
from logging.handlers import RotatingFileHandler

# Add your own conf dir
os.environ['HADOOP_CONF_DIR'] = os.path.abspath(os.getcwd()) + '/spark/conf'
os.environ['YARN_CONF_DIR'] = os.path.abspath(os.getcwd()) + '/spark/conf'
EXTRA_PACKAGES = "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0"

positive = [
    "upgrade",
    "upgraded",
    "long",
    "buy",
    "buying",
    "growth",
    "good",
    "gained",
    "well",
    "great",
    "nice",
    "top",
    "support",
    "update",
    "strong",
    "bullish",
    "bull",
    "highs",
    "win",
    "positive",
    "profits",
    "bonus",
    "potential",
    "success",
    "winner",
    "winning",
    "good"]

negative = [
    "downgraded",
    "bears",
    "bear",
    "bearish",
    "drop",
    "volatile",
    "short",
    "sell",
    "selling",
    "forget",
    "down",
    "resistance",
    "sold",
    "sellers",
    "negative",
    "selling",
    "blowout",
    "losses",
    "war",
    "lost",
    "loser"]


class StreamTwitterDataTransformer():
    def __init__(self, spark):
        self.spark = spark
        self.frequency = ['minute', 'hour', 'day', 'week', 'month', 'year']

    def map_time(self, df, frequency):
        return df.withColumn('recorded_time', date_trunc(
            frequency, col('recorded_time')))

    def analyze_statistics(self, df, frequency):
        def get_sentiment(tweet_content):
            for word in positive:
                if tweet_content.find(word) != -1:
                    return 1
            for word in negative:
                if tweet_content.find(word) != -1:
                    return -1
            return 0

        get_sentiment_udf = udf(lambda content: get_sentiment(content), IntegerType())
        df = df.withColumn('sentiment', get_sentiment_udf(col('content')))
        df = df.groupBy('symbol', 'recorded_time')\
               .agg(count('content').alias('count'),
                    sum('sentiment').alias('sentiment'))

        df = df.select(col('symbol'), col('recorded_time'),
                       col('count'), lit(frequency).alias('frequency'), col('sentiment'))
        return df

    def transform_data(self, df):
        frequency_dfs = {f: self.map_time(df, f) for f in self.frequency}
        frequency_dfs = {f: self.analyze_statistics(df, f) for f, df in frequency_dfs.items()}
        # This only work because I'm in a hurry. If database to big it will explode
        result_df = self.spark.read.format('org.apache.spark.sql.cassandra')\
            .options(table='stream_tweet_trending', keyspace='coinhub')\
            .load()
        for frequency_df in frequency_dfs.values():
            frequency_df = frequency_df.filter(col('recorded_time').isNotNull())
            result_df = result_df.union(frequency_df)\
                .groupBy('symbol', 'recorded_time', 'frequency')\
                .agg(sum('count').alias('count'),
                     sum('sentiment').alias('sentiment'))
            # Cassandra requires cols in alphabet order
            result_df = result_df.select(['symbol', 'recorded_time', *sorted(result_df.columns[2:])])
        return result_df


class StreamTwitterDataAnalyzer():
    def __init__(self):
        log_handler = RotatingFileHandler(
            f"{os.path.abspath(os.getcwd())}/spark/streaming/logs/analyzer.log",
            maxBytes=104857600, backupCount=10)
        logging.basicConfig(
            format='%(asctime)s,%(msecs)d <%(name)s>[%(levelname)s]: %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG,
            handlers=[log_handler])

        self.spark = SparkSession.builder\
            .config("spark.app.name", "StreamTwitterDataAnalyzer")\
            .config("spark.master", "local[*]")\
            .config("spark.jars.packages", EXTRA_PACKAGES)\
            .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions")\
            .config("spark.cassandra.connection.host", "172.20.0.15")\
            .config("spark.driver.host", "127.0.0.1")\
            .config("spark.cassandra.auth.username", "cassandra")\
            .config("spark.cassandra.auth.password", "cassandra")\
            .getOrCreate()
        # Options if my computer is better...
        #  .config("spark.driver.memory", "2g")\
        #  .config("spark.executor.memory", "2g")\
        #  .config("spark.executor.instances", "2")\
        self.logger = logging.getLogger('stream_twitter_analyzer')
        self.transformer = StreamTwitterDataTransformer(self.spark)

    def transform_and_save_data(self, df):
        self.logger.info('Start transforming data')
        frequency_df = self.transformer.transform_data(df)
        frequency_df.write.format('org.apache.spark.sql.cassandra')\
                          .mode('append')\
                          .options(table='stream_tweet_trending', keyspace='coinhub')\
                          .save()

    def analyze_data(self, df, batch_id):
        self.logger.info('Start analyzing at '
                         + datetime.now().strftime('%Y/%-m/%-d'))
        df = df.select(decode(col('value'), 'UTF-8').alias('value'),
                       col('timestamp').alias('recorded_time'))
        df = df.withColumn('symbol', translate(split(col('value'), '","').getItem(0), '"', ''))
        df = df.select(col('symbol'), col('recorded_time'),
                       col('value').substr(
                           length('symbol') + lit(5), length('value') - length('symbol') - 5)
                       .alias('content'))
        df = df.drop('value').na.drop('any')
        df.write.format('org.apache.spark.sql.cassandra')\
          .mode('append')\
          .options(table='recent_tweet', keyspace='coinhub')\
          .save()
        self.transform_and_save_data(df)

    def run(self):
        self.logger.info('Start analyzing twitter data from hdfs')
        df = self.spark.readStream.format('kafka')\
            .option('kafka.bootstrap.servers', 'localhost:19092,localhost:29092,localhost:39092')\
            .option('subscribe', 'twitterData')\
            .load()
        # .option('startingOffsets', 'earliest')\ # Using this when u need to write data from the beginning
        df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
        df.writeStream.foreachBatch(self.analyze_data).start().awaitTermination()
