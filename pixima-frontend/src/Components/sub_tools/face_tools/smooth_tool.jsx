import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { FaceRetouchingNatural } from "@mui/icons-material";
import "../../../Css/face_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class SmoothTool extends Component {
  state = {};
  smoothToolClickEvent = () => {
    this.props.onClick(ToolsIndices.SubTools.SmoothFaceTool)

  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.smoothToolClickEvent}
      >
        <FaceRetouchingNatural className="smooth-tool" />
      </IconButton>
    );
  }
}
