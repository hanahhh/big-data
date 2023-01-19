import axios from "axios";

const API_ROOT = process.env.REACT_APP_API_ROOT || "";

const APIS = {
    getOverviewInfo: () => axios.get(`${API_ROOT}/get_overview`),
    getTrendingSymbols: (args) =>
        axios.get(`${API_ROOT}/get_trending_symbols`, { params: args }),
    getSymbolTweets: (symbol, args) =>
        axios.get(`${API_ROOT}/get_symbol_tweets/${symbol}`, { params: args }),
    getSymbolCorrelation: (symbol, args) =>
        axios.get(`${API_ROOT}/get_symbol_correlation/${symbol}`, { params: args }),
};

export default APIS;
