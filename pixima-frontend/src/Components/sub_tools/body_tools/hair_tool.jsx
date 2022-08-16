import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import "../../../Css/body_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";

export class HairTool extends Component {
  state = {};
  hairToolClickEvent = () => {    this.props.onClick(ToolsIndices.SubTools.HairColorTool)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.hairToolClickEvent}
      >
        <img src={require("../../../images/Hair.png")}  alt="Color Clothe" width={26} height={26}  className="hair-tool" />
      </IconButton>
    );
  }
}
