import React from "react";
import { observer } from "mobx-react";
import { toJS } from "mobx";
import { Default } from "react-awesome-spinners";
import DatePicker from "react-datepicker";
import _ from "lodash";
import {
    ResponsiveContainer,
    BarChart,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip,
    Bar,
    Cell,
} from "recharts";
import topTrendStore from "./topTrendStore";
import "react-datepicker/dist/react-datepicker.css";
import "./styles.css";

class TopTrending extends React.Component {
    getSymbolChartCell() {
        return topTrendStore.symbolChartCellColor.map((color, index) => (
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
        const store = topTrendStore;
        const symbolChartData = toJS(store.trendingSymbols);

        if (store.isLoading) return <Default />;

        return (
            <div className="top-trending-view">
                <div className="chart-view">
                    <div className="chart-title">Top trending symbols</div>
                    <div className="time-picker">
                        <div className="time-picker-text">From</div>
                        <div className="time-picker-select">
                            <DatePicker
                                selected={store.startTimeTrending}
                                onChange={(time) =>
                                    store.setStartTimeTrending(time)
                                }
                                timeInputLabel="Time:"
                                dateFormat="MM/dd/yyyy h:mm aa"
                                showTimeInput
                            />
                        </div>
                        <div className="time-picker-text">to</div>
                        <div className="time-picker-select">
                            <DatePicker
                                selected={store.endTimeTrending}
                                onChange={(time) =>
                                    store.setEndTimeTrending(time)
                                }
                                timeInputLabel="Time:"
                                dateFormat="MM/dd/yyyy h:mm aa"
                                showTimeInput
                            />
                        </div>
                        <button
                            className="btn btn-primary"
                            onClick={store.fetchTrendingSymbols.bind(store)}
                        >
                            Get
                        </button>
                    </div>
                    <ResponsiveContainer width="100%" height={800}>
                        <BarChart
                            width={600}
                            layout="vertical"
                            height={600}
                            margin={{
                                top: 40,
                                right: 40,
                                left: 50,
                                bottom: 40,
                            }}
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
                    </ResponsiveContainer>
                </div>
            </div>
        );
    }
}

export default observer(TopTrending);
