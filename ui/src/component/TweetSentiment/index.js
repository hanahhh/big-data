import React from "react";
import { observer } from "mobx-react";
import { Default } from "react-awesome-spinners";
import tweetSentimentStore from "./tweetSentimentStore";
import TweetSentimentChart from "./tweetSentimentChart";
import "./styles.css";

class TweetSentiment extends React.Component {
    render() {
        const store = tweetSentimentStore;
        const symbolTweets = tweetSentimentStore.symbolTweets;

        return (
            <div className="tweet-sentiment-view">
                <div className="symbol-select">
                    <input
                        type="text"
                        id="symbol-input"
                        name="symbol-input"
                        placeholder="Sample: BTCUSDT"
                        value={store.symbol}
                        onChange={(e) => store.setSymbol(e.target.value)}
                    />
                    <button
                        className="btn btn-primary symbol-btn"
                        onClick={store.fetchSymbolTweets.bind(store)}
                    >
                        Get
                    </button>
                </div>
                <div className="tweet-sentiment-title">
                    Number of tweets/Sentiment for {store.symbol}
                </div>
                <div className="frequency-view">
                    <div>Zoom:</div>
                    <button
                        className={`btn btn-outline-secondary frequency-btn shadow-none${
                            store.frequency === "minute" ? " active" : ""
                        }`}
                        onClick={(e) => {
                            store.setFrequency("minute");
                            store.fetchSymbolTweets();
                        }}
                    >
                        All
                    </button>
                    <button
                        className={`btn btn-outline-secondary frequency-btn shadow-none${
                            store.frequency === "hour" ? " active" : ""
                        }`}
                        onClick={(e) => {
                            store.setFrequency("hour");
                            store.fetchSymbolTweets();
                        }}
                    >
                        1H
                    </button>
                    <button
                        className={`btn btn-outline-secondary frequency-btn shadow-none${
                            store.frequency === "day" ? " active" : ""
                        }`}
                        onClick={(e) => {
                            store.setFrequency("day");
                            store.fetchSymbolTweets();
                        }}
                    >
                        1D
                    </button>
                    <button
                        className={`btn btn-outline-secondary frequency-btn shadow-none${
                            store.frequency === "week" ? " active" : ""
                        }`}
                        onClick={(e) => {
                            store.setFrequency("week");
                            store.fetchSymbolTweets();
                        }}
                    >
                        1W
                    </button>
                    <button
                        className={`btn btn-outline-secondary frequency-btn shadow-none${
                            store.frequency === "month" ? " active" : ""
                        }`}
                        onClick={(e) => {
                            store.setFrequency("month");
                            store.fetchSymbolTweets();
                        }}
                    >
                        1M
                    </button>
                    <button
                        className={`btn btn-outline-secondary frequency-btn shadow-none${
                            store.frequency === "year" ? " active" : ""
                        }`}
                        onClick={(e) => {
                            store.setFrequency("year");
                            store.fetchSymbolTweets();
                        }}
                    >
                        1Y
                    </button>
                </div>
                {store.isLoading && <Default />}
                {!store.isLoading && <TweetSentimentChart data={symbolTweets} />}
            </div>
        );
    }
}

export default observer(TweetSentiment);
