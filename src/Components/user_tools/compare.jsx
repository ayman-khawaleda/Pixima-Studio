import React, { Component } from "react";
import { Compare } from "@mui/icons-material";
import IconButton from "@mui/material/IconButton";
import "../../Css/user-buttons.css"
import { ToolsIndices } from "../../ToolsIndices";
export class CompareButton extends Component {
  state = {};

  CompareClickEvent = () => {
    this.props.onClick(ToolsIndices.UserTool.CompareTool)
  };

  render() {
    return (
      <IconButton
        color="primary"
        aria-label="upload picture"
        component="label"
        onClick={this.CompareClickEvent}
      >
        <Compare className="compareIcon" />
      </IconButton>
    );
  }
}
