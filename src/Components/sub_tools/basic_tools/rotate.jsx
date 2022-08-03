import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { FlipCameraAndroid } from "@mui/icons-material";
import "../../../Css/basic_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class RotateTool extends Component {
  state = {};
  rotateToolClickEvent = () => {    this.props.onClick(ToolsIndices.SubTools.RotateTool)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.rotateToolClickEvent}
      >
        <FlipCameraAndroid className="rotate-tool" />
      </IconButton>
    );
  }
}
