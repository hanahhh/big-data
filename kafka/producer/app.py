from producer import StockProducer
from realtimeProducer import RealtimeStockProducer


def run_services():
    # producer = StockProducer()
    # producer.run()
    realtimeProducer = RealtimeStockProducer()
    realtimeProducer.run()


run_services()
