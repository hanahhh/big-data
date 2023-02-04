from consumer import StockConsumer
from realtimeConsumer import RealtimeStockConsumer


def run_services():
    # consumer = StockConsumer()
    # consumer.run()
    realtimeConsumer = RealtimeStockConsumer()
    realtimeConsumer.run()


run_services()
