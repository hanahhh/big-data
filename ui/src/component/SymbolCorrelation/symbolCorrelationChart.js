import React from "react";
import { observer } from "mobx-react";
import _ from "lodash";
import {
    ResponsiveContainer,
    ComposedChart,
    BarChart,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip,
    Legend,
    Bar,
    ErrorBar,
    Line,
} from "recharts";

class SymbolCorrelationChart extends React.Component {
    customCandleTooltip({ active, payload, label }) {
        if (active && payload && payload.length) {
            const data = payload[0].payload
            return (
                <div className="custom-tooltip">
                    <p className="tooltip-label">
                        {new Date(label).toLocaleString("vn-VN", {
                            hour12: false,
                        })}
                    </p>
                    <p className="tooltip-value">{`Open: ${data.open}`}</p>
                    <p className="tooltip-value">{`High: ${data.high}`}</p>
                    <p className="tooltip-value">{`Low: ${data.low}`}</p>
                    <p className="tooltip-value">{`Close: ${data.close}`}</p>
                    <p className="tooltip-value">{`Volume: ${payload[1].value}`}</p>
                </div>
            );
        }

        return null;
    }

    customTooltip({ active, payload, label }) {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip">
                    <p className="tooltip-label">
                        {new Date(label).toLocaleString("vn-VN", {
                            hour12: false,
                        })}
                    </p>
                    {_.map(payload, (p) => (
                        <p className="tooltip-value">{`${p.name}: ${p.value}`}</p>
                    ))}
                </div>
            );
        }

        return null;
    }

    renderLegendText(value, entry) {
        const { color } = entry;
        if(value === "oc") value = 'o h l c'
        return <span style={{ color }}>{_.startCase(value)}</span>;
    }

    formatXAxis(tickItem) {
        return new Date(tickItem).toLocaleString("vn-VN", { hour12: false });
    }

    render() {
        return (
            <div>
                <ResponsiveContainer width="100%" height={300}>
                    <ComposedChart
                        width={600}
                        height={300}
                        syncId="symbol-correlation-chart"
                        margin={{
                            top: 40,
                            right: 40,
                            left: 40,
                            bottom: 40,
                        }}
                        data={this.props.symbolData}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                            dataKey="recorded_time"
                            tickFormatter={this.formatXAxis}
                        />
                        <YAxis
                            yAxisId="left"
                            type="number"
                            domain={[
                                this.props.priceDomain.min,
                                this.props.priceDomain.max,
                            ]}
                        />
                        <YAxis
                            dataKey="volume"
                            yAxisId="right"
                            orientation="right"
                            type="number"
                        />
                        <Tooltip content={this.customCandleTooltip} />
                        <Legend
                            verticalAlign="top"
                            height={36}
                            formatter={this.renderLegendText}
                        />
                        <Bar yAxisId="left" dataKey="oc" fill="#d89584">
                            <ErrorBar
                                dataKey="hl"
                                width={4}
                                strokeWidth={2}
                                stroke="#d89584"
                                direction="y"
                            />
                        </Bar>
                        <Line
                            yAxisId="right"
                            type="monotone"
                            dataKey="volume"
                            stroke="#848fd8"
                            dot={false}
                        />
                    </ComposedChart>
                </ResponsiveContainer>
                <ResponsiveContainer width="100%" height={300}>
                    <BarChart
                        width={600}
                        height={300}
                        syncId="symbol-correlation-chart"
                        margin={{
                            top: 40,
                            right: 40,
                            left: 40,
                            bottom: 40,
                        }}
                        data={this.props.tweetData}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                            dataKey="recorded_time"
                            tickFormatter={this.formatXAxis}
                        />
                        <YAxis type="number" />
                        <Tooltip content={this.customTooltip} />
                        <Legend
                            verticalAlign="bottom"
                            height={36}
                            formatter={this.renderLegendText}
                        />
                        <Bar
                            dataKey="tweet_count"
                            maxBarSize={30}
                            fill="#d8be84"
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        );
    }
}

export default observer(SymbolCorrelationChart);
