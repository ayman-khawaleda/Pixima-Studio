import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { Contrast } from "@mui/icons-material";
import "../../../Css/basic_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class ContrastTool extends Component {
  state = {};
  contrastToolClickEvent = () => {
    this.props.onClick(ToolsIndices.SubTools.ContrastTool)

  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.contrastToolClickEvent}
      >
        <Contrast className="contrast-tool" />
      </IconButton>
    );
  }
}
