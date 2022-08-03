import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import "../../../Css/face_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class ResizeEyeTool extends Component {
  state = {};
  eyeResizeToolClickEvent = () => {
    this.props.onClick(ToolsIndices.SubTools.EyeResizeTool)

  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.eyeResizeToolClickEvent}
      >
        <img src={require("../../../images/Eye.png")}  alt="Eye Resize" width={24} height={24}  className="eye-resize-tool" />
      </IconButton>
    );
  }
}
