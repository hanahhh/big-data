import React from "react";
import { observer } from "mobx-react";
import _ from "lodash";
import {
    ResponsiveContainer,
    AreaChart,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip,
    Legend,
    Area,
} from "recharts";

class TweetSentimentChart extends React.Component {
    customTooltip({ active, payload, label }) {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip">
                    <p className="tooltip-label">
                        {new Date(label).toLocaleString("vn-VN", {
                            hour12: false,
                        })}
                    </p>
                    <p className="tooltip-value">{`${_.startCase(
                        payload[0].name
                    )}: ${payload[0].value}`}</p>
                    <p className="tooltip-value">{`${_.startCase(
                        payload[1].name
                    )}: ${payload[1].value}`}</p>
                </div>
            );
        }

        return null;
    }

    renderLegendText(value, entry) {
        const { color } = entry;
      
        return <span style={{ color }}>{_.startCase(value)}</span>;
      };

    formatXAxis(tickItem) {
        return new Date(tickItem).toLocaleString("vn-VN", { hour12: false });
    }

    render() {
        return (
            <div>
                <ResponsiveContainer width="100%" height={800}>
                    <AreaChart
                        width={600}
                        height={600}
                        margin={{
                            top: 40,
                            right: 40,
                            left: 10,
                            bottom: 40,
                        }}
                        data={this.props.data}
                    >
                        <defs>
                            <linearGradient
                                id="colorTweetCount"
                                x1="0"
                                y1="0"
                                x2="0"
                                y2="1"
                            >
                                <stop
                                    offset="5%"
                                    stopColor="#8884d8"
                                    stopOpacity={0.8}
                                />
                                <stop
                                    offset="95%"
                                    stopColor="#8884d8"
                                    stopOpacity={0}
                                />
                            </linearGradient>
                            <linearGradient
                                id="colorSentiment"
                                x1="0"
                                y1="0"
                                x2="0"
                                y2="1"
                            >
                                <stop
                                    offset="5%"
                                    stopColor="#82ca9d"
                                    stopOpacity={0.8}
                                />
                                <stop
                                    offset="95%"
                                    stopColor="#82ca9d"
                                    stopOpacity={0}
                                />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                            dataKey="recorded_time"
                            tickFormatter={this.formatXAxis}
                        />
                        <YAxis type="number" />
                        <Tooltip content={this.customTooltip} />
                        <Legend verticalAlign="top" height={36} formatter={this.renderLegendText}/>
                        <Area
                            type="monotone"
                            dataKey="tweet_count"
                            stroke="#8884d8"
                            fillOpacity={1}
                            fill="url(#colorTweetCount)"
                        />
                        <Area
                            type="monotone"
                            dataKey="sentiment"
                            stroke="#82ca9d"
                            fillOpacity={1}
                            fill="url(#colorSentiment)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        );
    }
}

export default observer(TweetSentimentChart);
