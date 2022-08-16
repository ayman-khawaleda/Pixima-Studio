import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { TagFaces } from "@mui/icons-material";
import "../../../Css/face_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class SmileTool extends Component {
  state = {};
  smileToolClickEvent = () => {
    this.props.onClick(ToolsIndices.SubTools.SmileTool)

  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.smileToolClickEvent}
      >
        <TagFaces className="smile-tool" />
      </IconButton>
    );
  }
}
