import { Camera } from "@mui/icons-material";
import { IconButton } from "@mui/material";
import React, { Component } from "react";
import "../../Css/main_tools.css";
import { ToolsIndices } from "../../ToolsIndices";
export class BasicTools extends Component {
  state = {};
  basicToolsCliclEvent = () => {
    this.props.onClick(ToolsIndices.MainTool.BasicTools);
    this.props.setDefault(ToolsIndices.SubTools.FlipTool)
  };

  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.basicToolsCliclEvent}
      >
        <Camera className="basic-tools" />
      </IconButton>
    );
  }
}
