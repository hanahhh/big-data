import React from "react";
import Header from "../Header";
import { observer } from "mobx-react";
import { Switch, Route, withRouter } from "react-router-dom";
import { routingPaths } from "../../stores/routingStore";
import Overview from "../Overview";
import TopTrending from "../TopTrending";
import TweetSentiment from "../TweetSentiment";
import SymbolCorrelation from "../SymbolCorrelation";
import Home from "../Home";
import "./styles.css";

class App extends React.Component {
    render() {
        return (
            <div className="app">
                <Header />
                <div className="app-body">
                    <Switch>
                        <Route
                            exact
                            path={routingPaths.home}
                            component={Home}
                        />
                        <Route
                            path={routingPaths.overview}
                            component={Overview}
                        />
                        <Route
                            path={routingPaths.topTrending}
                            component={TopTrending}
                        />
                        <Route
                            path={routingPaths.tweetSentiment}
                            component={TweetSentiment}
                        />
                        <Route
                            path={routingPaths.symbolCorrelation}
                            component={SymbolCorrelation}
                        />
                    </Switch>
                </div>
            </div>
        );
    }
}

export default withRouter(observer(App));
