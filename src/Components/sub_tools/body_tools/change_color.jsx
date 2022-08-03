import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import "../../../Css/body_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class ChangeClotheColor extends Component {
  state = {};
  changeClotheColorToolClickEvent = () => {    this.props.onClick(ToolsIndices.SubTools.ChangeColorTool)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.changeClotheColorToolClickEvent}
      >
        <img src={require("../../../images/tshirt.png")}  alt="Color Clothe" width={24} height={24} className="change-clothe-color-tool" />
      </IconButton>
    );
  }
}
