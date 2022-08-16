import React, { Component } from "react";
import Favicon from "react-favicon";

export default class FavIcon extends Component {
  render() {
    return (
      <React.Fragment>
        <Favicon
          url={require("../images/PiximaLogo-Small.png")}
          animated={true}
        />
      </React.Fragment>
    );
  }
}
