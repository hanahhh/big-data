import React from "react";
import ReactDOM from "react-dom";
import App from "./component/App";
import { BrowserRouter } from "react-router-dom";
import "./styles.css";

ReactDOM.render(
    <React.StrictMode>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </React.StrictMode>,
    document.getElementById("root")
);
