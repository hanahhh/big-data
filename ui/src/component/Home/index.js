import React from "react";
import { observer } from "mobx-react";
import "./styles.css";

class Home extends React.Component {
    render() {
        return (
            <div className="home-page">
                <div className="home-text">Welcome to Coin Hub</div>
            </div>
        );
    }
}

export default observer(Home);
