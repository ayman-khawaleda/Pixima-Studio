import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import "../../../Css/face_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class NoseResizeTool extends Component {
  state = {};
  NoseResizeToolClickEvent = () => {  
      this.props.onClick(ToolsIndices.SubTools.NoseResizeTool)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.NoseResizeToolClickEvent}
      >
        <img src={require("../../../images/Nose.png")}  alt="white teeth" width={24} height={24}  className="nose-tool" />
      </IconButton>
    );
  }
}
