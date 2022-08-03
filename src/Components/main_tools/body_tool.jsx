import React, { Component } from "react";
import { IconButton } from "@mui/material";
import { ToolsIndices } from "../../ToolsIndices";
import { Accessibility } from "@mui/icons-material";
export class BodyTool extends Component {
  state = {};
  bodyToolEvent = () => {
    this.props.onClick(ToolsIndices.MainTool.BodyTools);
    this.props.setDefault(ToolsIndices.SubTools.ChangeColorTool)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.bodyToolEvent}
      >
        <Accessibility className = "body-tools"/>
      </IconButton>
    );
  }
}
