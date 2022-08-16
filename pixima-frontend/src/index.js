import React from "react";
import ReactDOM from "react-dom/client";
import {
  Body
} from "./Components/Body"
import FavIcon from "./Components/fav"
const root = ReactDOM.createRoot(document.getElementById("root"))

root.render( <React.Fragment> < Body / > <FavIcon/> </React.Fragment> )
