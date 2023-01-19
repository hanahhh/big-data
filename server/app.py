from datetime import datetime, timedelta
from flask import Flask, abort, request
from flask_cors import CORS
from cassandra.cluster import Cluster

cluster = Cluster(['172.20.0.15'])
session = cluster.connect('coinhub')

app = Flask(__name__)
CORS(app)


@app.route('/get_overview', methods=['GET'])
def get_overview():
    symbol_limit = request.args.get('symbol_limit') or 10
    tweet_limit = request.args.get('tweet_limit') or 10
    start_time = (datetime.utcnow() - timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
    tweets = session.execute('select recorded_time, content from recent_tweet')
    symbols = session.execute(
        f"select symbol, sum(count) as tweet_count, sum(sentiment) as total_sentiment from stream_tweet_trending where recorded_time >= '{start_time}' and frequency = 'minute' group by symbol allow filtering")

    result = {'symbols': [], 'tweets': []}
    for tweet in tweets:
        result['tweets'].append(
            {'recorded_time': tweet.recorded_time,
             'content': tweet.content})
    for symbol in symbols:
        color = "#5C5CFF"  # blue
        if symbol.total_sentiment > 0:
            color = "#5CFF5C"  # green
        elif symbol.total_sentiment < 0:
            color = "#FF5C5C"  # red
        result['symbols'].append(
            {'symbol': symbol.symbol,
             'tweet_count': symbol.tweet_count,
             'color': color})

    result['tweets'] = sorted(result['tweets'], key=lambda t: t['recorded_time'], reverse=True)[:tweet_limit]
    result['symbols'] = sorted(result['symbols'], key=lambda t: t['tweet_count'], reverse=True)[:symbol_limit]

    return result


@app.route('/get_trending_symbols', methods=['GET'])
def get_trending_symbols():
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')
    if not start_time or not end_time:
        abort(400, 'You haven\'t entered enough start time and end time')

    start_time = datetime\
        .strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f%z')\
        .strftime('%Y-%m-%d %H:%M:%S.%f%z')
    end_time = datetime\
        .strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f%z')\
        .strftime('%Y-%m-%d %H:%M:%S.%f%z')
    # In real scenario this should take from tweet_trending table
    symbols = session.execute(
        f"select symbol, sum(count) as tweet_count, sum(sentiment) as total_sentiment from stream_tweet_trending where recorded_time >= '{start_time}' and recorded_time <= '{end_time}' and frequency = 'minute' group by symbol allow filtering")

    result = {'symbols': []}
    for symbol in symbols:
        color = "#5C5CFF"  # blue
        if symbol.total_sentiment > 0:
            color = "#5CFF5C"  # green
        elif symbol.total_sentiment < 0:
            color = "#FF5C5C"  # red
        result['symbols'].append(
            {'symbol': symbol.symbol,
             'tweet_count': symbol.tweet_count,
             'color': color})

    result['symbols'] = sorted(result['symbols'], key=lambda t: t['tweet_count'], reverse=True)

    return result


@app.route('/get_symbol_tweets/<symbol>', methods=['GET'])
def get_symbol_tweets(symbol):
    frequency = request.args.get('frequency')
    if not frequency:
        abort(400, 'You haven\'t entered frequency')

    # In real scenario this should take from tweet_trending table
    tweets = session.execute(
        f"select recorded_time, count, sentiment from stream_tweet_trending where symbol = '{symbol.lower()}' and frequency = '{frequency}' allow filtering")
    result = {'tweets': []}
    for tweet in tweets:
        result['tweets'].append(
            {'recorded_time': tweet.recorded_time,
             'tweet_count': tweet.count,
             'sentiment': tweet.sentiment})
    result['tweets'] = sorted(result['tweets'], key=lambda t: t['recorded_time'])
    return result


@app.route('/get_symbol_correlation/<symbol>', methods=['GET'])
def get_symbol_correlation(symbol):
    frequency = request.args.get('frequency')
    if not frequency:
        abort(400, 'You haven\'t entered frequency')

    tweets = session.execute(
        f"select recorded_time, count from stream_tweet_trending where symbol = '{symbol.lower()}' and frequency = '{frequency}' allow filtering")
    symbols = session.execute(
        f"select recorded_time, high, low, open, close, volume from coin_data where symbol = '{symbol}' and frequency = '{frequency}' allow filtering")

    tweet_over_time = {}
    result = {'symbol_correlation': []}
    for tweet in tweets:
        tweet_over_time[tweet.recorded_time.strftime('%Y-%m-%d %H:%M:%S.%f%z')] = tweet.count

    for symbol_data in symbols:
        tweet_count = 0
        if symbol_data.recorded_time.strftime('%Y-%m-%d %H:%M:%S.%f%z') in tweet_over_time:
            tweet_count = tweet_over_time[symbol_data.recorded_time.strftime('%Y-%m-%d %H:%M:%S.%f%z')]
        result['symbol_correlation'].append({
            'recorded_time': symbol_data.recorded_time,
            'high': symbol_data.high,
            'low': symbol_data.low,
            'open': symbol_data.open,
            'close': symbol_data.close,
            'volume': symbol_data.volume,
            'tweet_count': tweet_count,
        })
    result['symbol_correlation'] = sorted(result['symbol_correlation'], key=lambda t: t['recorded_time'])

    return result


if __name__ == "__main__":
    app.run(debug=True)
