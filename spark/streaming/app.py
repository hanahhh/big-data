from analyzer import StreamTwitterDataAnalyzer


def run_service():
    analyzer = StreamTwitterDataAnalyzer()
    analyzer.run()


run_service()
