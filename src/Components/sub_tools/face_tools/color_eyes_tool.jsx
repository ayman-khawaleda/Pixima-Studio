import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import "../../../Css/face_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class ColorEyeTool extends Component {
  state = {};
  eyeColorToolClickEvent = () => {    this.props.onClick(ToolsIndices.SubTools.EyeColorTool)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.eyeColorToolClickEvent}
      >
        <img src={require("../../../images/Eye.png")}  alt="Eye Color" width={24} height={24}  className="eye-color-tool" />
      </IconButton>
    );
  }
}
