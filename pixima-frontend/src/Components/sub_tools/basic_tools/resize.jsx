import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { ImageAspectRatio } from "@mui/icons-material";
import "../../../Css/basic_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class ResizeTool extends Component {
  state = {};
  resizeToolClickEvent = () => {
    this.props.onClick(ToolsIndices.SubTools.ResizeTool)

  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.resizeToolClickEvent}
      >
        <ImageAspectRatio className="resize-tool" />
      </IconButton>
    );
  }
}
