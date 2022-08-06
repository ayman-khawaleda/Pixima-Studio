import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { Crop } from "@mui/icons-material";
import "../../../Css/basic_tools.css";
import  { ToolsIndices } from "../../../ToolsIndices"
export class CropTool extends Component {
  state = {};
  cropToolClickEvent = () => {
    this.props.onClick(ToolsIndices.SubTools.CropTool)
    console.log(this.props)
    console.log(this.props)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.cropToolClickEvent}
      >
        <Crop className="crop-tool" />
      </IconButton>
    );
  }
}
