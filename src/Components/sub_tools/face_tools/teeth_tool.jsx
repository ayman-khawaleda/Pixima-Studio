import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import "../../../Css/face_tools.css";
import { ToolsIndices } from "../../../ToolsIndices";

export class TeethTool extends Component {
  state = {};
  teethToolClickEvent = () => {
    this.props.onClick(ToolsIndices.SubTools.WhiteTeethTool)

  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.teethToolClickEvent}
      >
        <img src={require("../../../images/teeth.png")}  alt="white teeth" width={24} height={24}  className="teeth-tool" />
      </IconButton>
    );
  }
}
