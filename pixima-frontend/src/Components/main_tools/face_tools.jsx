import { Face } from "@mui/icons-material";
import { IconButton } from "@mui/material";
import React, { Component } from "react";
import "../../Css/main_tools.css";
import { ToolsIndices } from "../../ToolsIndices";

export class FaceTools extends Component {
  state = {};
  faceToolClickEvent = () => {
      this.props.onClick(ToolsIndices.MainTool.FaceTools);
      this.props.setDefault(ToolsIndices.SubTools.SmileTool)
  }
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={() => {
          this.faceToolClickEvent();
        }}
      >
        <Face className="face-tools" />
      </IconButton>
    );
  }
}
