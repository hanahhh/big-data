import React from "react";
import logo from "./logo.png";
import { NavLink } from "react-router-dom";
import { observer } from "mobx-react";
import { routingPaths } from "../../stores/routingStore";
import "./styles.css";

class Header extends React.Component {
  render() {
    return (
      <div>
        <div className="header">
          <a className="header-link" href="/">
            <p className="logo-text" style={{ fontWeight: "bold" }}>
              Stock market
            </p>
          </a>
          <div className="header-btn">
            <NavLink className="header-btn-link" to={routingPaths.topTrending}>
              Statistic
            </NavLink>
          </div>
          <div className="header-btn">
            <NavLink
              className="header-btn-link"
              to={routingPaths.tweetSentiment}
            >
              Tweet Sentiment
            </NavLink>
          </div>
          <div className="header-btn last-header-btn">
            <NavLink
              className="header-btn-link"
              to={routingPaths.symbolCorrelation}
            >
              Symbol Correlation
            </NavLink>
          </div>
        </div>
      </div>
    );
  }
}

export default observer(Header);
