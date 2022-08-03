import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import "../../../Css/sub_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class SaturationTool extends Component {
  state = {};
  saturationToolClickEvent = () => {    this.props.onClick(ToolsIndices.SubTools.SaturationTool)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.saturationToolClickEvent}
      >
        <img
          src={require("../../../images/saturation.png")}
          className="saturation-tool"
          alt="Saturation-Tool"
          width={24}
          height={24}
        />
      </IconButton>
    );
  }
}
