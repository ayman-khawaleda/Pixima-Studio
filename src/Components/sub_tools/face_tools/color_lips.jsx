import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import "../../../Css/face_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class ColorLipsTool extends Component {
  state = {};
  colorLipsToolClickEvent = () => {    this.props.onClick(ToolsIndices.SubTools.ColorLipsTool)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.colorLipsToolClickEvent}
      >
        <img src={require("../../../images/Lips.png")}  alt="Lips" width={24} height={24}  className="lips-tool" />
      </IconButton>
    );
  }
}
