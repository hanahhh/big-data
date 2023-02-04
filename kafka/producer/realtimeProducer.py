import logging
from logging.handlers import RotatingFileHandler
from kafka import KafkaProducer
from kafka.errors import KafkaError
import os
from vnstock import *
from datetime import date, timedelta


class RealtimeStockProducer:
    def __init__(self):
        log_handler = RotatingFileHandler(
            f"{os.path.abspath(os.getcwd())}/kafka/producer/logs/producer.log",
            maxBytes=104857600, backupCount=10)
        logging.basicConfig(
            format='%(asctime)s,%(msecs)d <%(name)s>[%(levelname)s]: %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG,
            handlers=[log_handler])
        self.logger = logging.getLogger('realtimeProducer')

        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:19092'],
            client_id='producer')

    def message_handler(self, message):
        #  Message from stock api
        try:
            print(
                "___________________________________________________________________" + message)
            self.producer.send('realtimeStockData', bytes(
                message, encoding='utf-8'))
            self.producer.flush()
        except KafkaError as e:
            self.logger.error(f"An Kafka error happened: {e}")
        except Exception as e:
            self.logger.error(
                f"An error happened while pushing message to Kafka: {e}")

    def crawl_from_binance(self, symbol_list):
        try:
            self.logger.info("Start running realtime stock producer...")
            for idx, symbol in enumerate(symbol_list):
                print(symbol)
                data = stock_intraday_data(symbol=symbol,
                                           page_num=0,
                                           page_size=1)
                self.message_handler(data.to_json())
            while True:
                pass
        except Exception as e:
            self.logger.error(f"An error happened while streaming: {e}")

    def run(self):
        with open(os.path.abspath(os.getcwd()) + "/kafka/producer/symbol_list.csv") as f:
            symbol_list = f.read().split('\n')
        self.crawl_from_binance(symbol_list)
