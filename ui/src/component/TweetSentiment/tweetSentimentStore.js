import { action, makeObservable, observable } from "mobx";
import _ from "lodash";
import APIS from "../../services/common";

class TweetSentimentStore {
    symbol = "";
    frequency = "minute";
    isLoading = false;
    symbolTweets = [];

    constructor() {
        makeObservable(this, {
            symbol: observable,
            frequency: observable,
            isLoading: observable,
            symbolTweets: observable,
            setSymbol: action,
            setFrequency: action,
            fetchSymbolTweets: action,
        });
    }

    setSymbol(symbol) {
        this.symbol = symbol.trim().toUpperCase();
    }

    setFrequency(frequency) {
        this.frequency = frequency;
    }

    fetchSymbolTweets() {
        if (this.symbol === "") {
            window.alert("You haven't entered symbol");
            return;
        }

        this.isLoading = true;
        APIS.getSymbolTweets(this.symbol, { frequency: this.frequency }).then(
            (res) => {
                this.symbolTweets = _.map(res.data.tweets, (symbol) => ({
                    recorded_time: symbol.recorded_time,
                    sentiment: symbol.sentiment,
                    tweet_count: symbol.tweet_count,
                }));
                this.isLoading = false;
            }
        );
    }
}

export default new TweetSentimentStore();
