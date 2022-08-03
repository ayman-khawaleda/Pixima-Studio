import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { Flip } from "@mui/icons-material";
import "../../../Css/basic_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";

export class FlipTool extends Component {
  state = {}; 
  flipToolClickEvent = () => {
    this.props.onClick(ToolsIndices.SubTools.FlipTool)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.flipToolClickEvent}
      >
        <Flip className="flip-tool" />
      </IconButton>
    );
  }
}
