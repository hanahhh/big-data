import React from "react";
import { observer } from "mobx-react";
import { Default } from "react-awesome-spinners";
import symbolCorrelationStore from "./symbolCorrelationStore";
import SymbolCorrelationChart from "./symbolCorrelationChart";
import "./styles.css";

class SymbolCorrelation extends React.Component {
    render() {
        const store = symbolCorrelationStore;
        const symbolData = symbolCorrelationStore.symbolData;
        const tweetData = symbolCorrelationStore.tweetData;

        return (
            <div className="symbol-correlation-view">
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
                        onClick={store.fetchSymbolCorrelationData.bind(store)}
                    >
                        Get
                    </button>
                </div>
                <div className="symbol-correlation-title">
                    Symbol price/Mentions for {store.symbol}
                </div>
                <div className="frequency-view">
                    <div>Zoom:</div>
                    <button
                        className={`btn btn-outline-secondary frequency-btn shadow-none${
                            store.frequency === "minute" ? " active" : ""
                        }`}
                        onClick={(e) => {
                            store.setFrequency("minute");
                            store.fetchSymbolCorrelationData();
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
                            store.fetchSymbolCorrelationData();
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
                            store.fetchSymbolCorrelationData();
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
                            store.fetchSymbolCorrelationData();
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
                            store.fetchSymbolCorrelationData();
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
                            store.fetchSymbolCorrelationData();
                        }}
                    >
                        1Y
                    </button>
                </div>
                {store.isLoading && <Default />}
                {!store.isLoading && (
                    <SymbolCorrelationChart
                        symbolData={symbolData}
                        tweetData={tweetData}
                        priceDomain={store.priceDomain}
                    />
                )}
            </div>
        );
    }
}

export default observer(SymbolCorrelation);
