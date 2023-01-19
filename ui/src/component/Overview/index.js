import React from "react";
import { observer } from "mobx-react";
import { toJS } from "mobx";
import { Default } from "react-awesome-spinners";
import _ from "lodash";
import {
    BarChart,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip,
    Bar,
    Cell,
} from "recharts";
import overviewStore from "./overviewStore";
import "./styles.css";

class Overview extends React.Component {
    componentDidMount() {
        overviewStore.fetchOverviewInfo();
    }

    getLatestTweet() {
        const store = overviewStore;
        return (
            <div className="tweet-table">
                <div className="tweet-group">
                    <div className="tweet-value text-center">
                        <b>Top 10 latest tweets on Twitter</b>
                    </div>
                </div>
                {store.latestTweets.map((tweet) => (
                    <div className="tweet-group">
                        <div className="tweet-value">{tweet.content}</div>
                    </div>
                ))}
            </div>
        );
    }

    getSymbolChartCell() {
        return overviewStore.symbolChartCellColor.map((color, index) => (
            <Cell key={`cell-${index}`} fill={color} />
        ));
    }

    customTooltip({ active, payload, label }) {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip">
                    <p className="tooltip-label">{label}</p>
                    <p className="tooltip-value">{`${_.startCase(
                        payload[0].name
                    )}: ${payload[0].value}`}</p>
                </div>
            );
        }

        return null;
    }

    render() {
        const store = overviewStore;
        const symbolChartData = toJS(store.curTrendingSymbols);

        if (store.isLoading) return <Default />;

        return (
            <div className="overview">
                <div className="chart-view">
                    <div className="chart-title">
                        Top trending symbols in 10 minutes
                    </div>
                    <BarChart
                        width={600}
                        layout="vertical"
                        height={600}
                        margin={{ top: 40, right: 40, left: 50, bottom: 40 }}
                        data={symbolChartData}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" />
                        <YAxis
                            type="category"
                            dataKey="symbol"
                            tick={{ fontSize: 14 }}
                        />
                        <Tooltip content={this.customTooltip} />
                        <Bar
                            dataKey="tweet_count"
                            maxBarSize={30}
                            fill="#5C5CFF"
                        >
                            {this.getSymbolChartCell()}
                        </Bar>
                    </BarChart>
                </div>
                {this.getLatestTweet()}
            </div>
        );
    }
}

export default observer(Overview);
