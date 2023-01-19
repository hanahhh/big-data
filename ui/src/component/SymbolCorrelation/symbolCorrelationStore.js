import { action, makeObservable, observable } from "mobx";
import _ from "lodash";
import APIS from "../../services/common";

class SymbolCorrelationStore {
    symbol = "";
    frequency = "minute";
    isLoading = false;
    priceDomain = { max: 0, min: 1000000000 };
    symbolData = [];
    tweetData = [];

    constructor() {
        makeObservable(this, {
            symbol: observable,
            frequency: observable,
            isLoading: observable,
            symbolData: observable,
            tweetData: observable,
            priceDomain: observable,
            setSymbol: action,
            setFrequency: action,
            fetchSymbolCorrelationData: action,
        });
    }

    setSymbol(symbol) {
        this.symbol = symbol.trim().toUpperCase();
    }

    setFrequency(frequency) {
        this.frequency = frequency;
    }

    fetchSymbolCorrelationData() {
        if (this.symbol === "") {
            window.alert("You haven't entered symbol");
            return;
        }

        this.isLoading = true;
        APIS.getSymbolCorrelation(this.symbol, {
            frequency: this.frequency,
        }).then((res) => {
            this.symbolData = _.map(res.data.symbol_correlation, (symbol) => ({
                recorded_time: symbol.recorded_time,
                high: symbol.high,
                low: symbol.low,
                open: symbol.open,
                close: symbol.close,
                hl: [Math.min(symbol.open, symbol.close) - symbol.low, symbol.high - Math.min(symbol.open, symbol.close)],
                oc: [
                    Math.max(symbol.open, symbol.close),
                    Math.min(symbol.open, symbol.close),
                ],
                volume: symbol.volume,
                tweet_count: symbol.tweet_count,
            }));
            this.tweetData = _.map(res.data.symbol_correlation, (symbol) => ({
                recorded_time: symbol.recorded_time,
                tweet_count: symbol.tweet_count,
            }));
            _.forEach(res.data.symbol_correlation, (symbol) => {
                this.priceDomain.max = Math.max(this.priceDomain, 2*symbol.high);
                this.priceDomain.min = Math.min(this.priceDomain, 2*symbol.low);
            });
            this.isLoading = false;
        });
    }
}

export default new SymbolCorrelationStore();
