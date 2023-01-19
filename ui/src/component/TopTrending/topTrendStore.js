import { action, makeObservable, observable } from "mobx";
import _ from "lodash";
import APIS from "../../services/common";

class TopTrendStore {
    startTimeTrending = new Date();
    endTimeTrending = new Date();
    isLoading = false;
    trendingSymbols = [];
    symbolChartCellColor = [];

    constructor() {
        makeObservable(this, {
            startTimeTrending: observable,
            endTimeTrending: observable,
            isLoading: observable,
            trendingSymbols: observable,
            symbolChartCellColor: observable,
            setStartTimeTrending: action,
            setEndTimeTrending: action,
            fetchTrendingSymbols: action,
        });
    }

    setStartTimeTrending(time) {
        this.startTimeTrending = time;
    }

    setEndTimeTrending(time) {
        this.endTimeTrending = time;
    }

    fetchTrendingSymbols() {
        if (this.startTimeTrending === null){
            window.alert("You haven't entered input");
            return;
        }
        if (this.endTimeTrending === null) {
            window.alert("You haven't entered out");
            return;
        }
        if (this.endTimeTrending < this.startTimeTrending) {
            window.alert("End time need to be not smaller than start time");
            return;
        }

        this.isLoading = true;
        APIS.getTrendingSymbols({
            startTime: this.startTimeTrending,
            endTime: this.endTimeTrending,
        }).then((res) => {
            this.trendingSymbols = _.map(res.data.symbols, (symbol) => ({
                symbol: symbol.symbol.toUpperCase(),
                tweet_count: symbol.tweet_count,
            }));
            this.symbolChartCellColor = _.map(
                res.data.symbols,
                (symbol) => symbol.color
            );
            this.isLoading = false;
        });
    }
}

export default new TopTrendStore();
