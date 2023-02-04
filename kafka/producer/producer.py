import logging
from logging.handlers import RotatingFileHandler
from kafka import KafkaProducer
from kafka.errors import KafkaError
import os
from vnstock import *
from datetime import date, timedelta


class StockProducer:
    def __init__(self):
        log_handler = RotatingFileHandler(
            f"{os.path.abspath(os.getcwd())}/kafka/producer/logs/producer.log",
            maxBytes=104857600, backupCount=10)
        logging.basicConfig(
            format='%(asctime)s,%(msecs)d <%(name)s>[%(levelname)s]: %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG,
            handlers=[log_handler])
        self.logger = logging.getLogger('producer')

        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:19092',
                               'localhost:29092', 'localhost:39092'],
            client_id='producer')

    def message_handler(self, symbol, message):
        #  Message from stock api
        try:
            stock_info = f"{symbol},{message.Open.iloc[0]},{message.High.iloc[0]},{message.Low.iloc[0]},{message.Close.iloc[0]},{message.Volume.iloc[0]},{message.TradingDate.iloc[0]}"
            self.producer.send('stockData', bytes(
                stock_info, encoding='utf-8'))
            self.producer.flush()
        except KafkaError as e:
            self.logger.error(f"An Kafka error happened: {e}")
        except Exception as e:
            self.logger.error(
                f"An error happened while pushing message to Kafka: {e}")

    def crawl_from_binance(self, symbol_list):
        try:
            self.logger.info("Start running stock producer...")
            for idx, symbol in enumerate(symbol_list):
                start_date = (date.today() - timedelta(days=2)
                              ).strftime("%Y-%m-%d")
                end_date = (date.today() - timedelta(days=1)
                            ).strftime("%Y-%m-%d")
                print(symbol, start_date, end_date)
                data = stock_historical_data(symbol=symbol,
                                             start_date=start_date,
                                             end_date=end_date)

                self.message_handler(symbol, data)
            while True:
                pass
        except Exception as e:
            self.logger.error(f"An error happened while streaming: {e}")

    def run(self):
        with open(os.path.abspath(os.getcwd()) + "/kafka/producer/symbol_list.csv") as f:
            symbol_list = f.read().split('\n')
        self.crawl_from_binance(symbol_list)
