import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import "../../Css/user-buttons.css"
import { ToolsIndices } from "../../ToolsIndices";
import { ZoomIn } from "@mui/icons-material"
export class ZoomButton extends Component {
  state = {};

  ZoomClickEvent = () => {
    
    this.props.onClick(ToolsIndices.UserTool.ZoomTool)
  };

  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.ZoomClickEvent}
      >
        <ZoomIn className="zoomIcon" />
      </IconButton>
    );
  }
}
