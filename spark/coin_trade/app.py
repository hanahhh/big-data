import sys
from analyzer import CoinTradeDataAnalyzer


def run_service(start_date, start_file):
    analyzer = CoinTradeDataAnalyzer(start_date, start_file)
    analyzer.run()


if len(sys.argv) > 2:
    run_service(sys.argv[1], sys.argv[2])
elif len(sys.argv) > 1:
    run_service(sys.argv[1], None)
else:
    raise RuntimeError("Start date must be specific")
