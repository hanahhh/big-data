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
            f"{os.path.abspath(os.getcwd())}/kafka/realtimeProducer/logs/producer.log",
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

    def message_handler(self, symbol, message):
        #  Message from stock api
        try:
            stock_realtime_info = f"{symbol},{message.volume.iloc[0]},{message.cp.iloc[0]},{message.rcp.iloc[0]},{message.a.iloc[0]},{message.ba.iloc[0]},{message.sa.iloc[0]},{message.hl.iloc[0]},{message.pcp.iloc[0]},{message.time.iloc[0]}"
            print(stock_realtime_info)
            self.producer.send('realtimeStockData', bytes(
                stock_realtime_info, encoding='utf-8'))
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
                data = stock_intraday_data(symbol=symbol,
                                           page_num=0,
                                           page_size=1)
                self.message_handler(symbol, data)
            while True:
                pass
        except Exception as e:
            self.logger.error(f"An error happened while streaming: {e}")

    def run(self):
        with open(os.path.abspath(os.getcwd()) + "/kafka/producer/symbol_list.csv") as f:
            symbol_list = f.read().split('\n')
        self.crawl_from_binance(symbol_list)
