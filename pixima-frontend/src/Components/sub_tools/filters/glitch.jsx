import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { Filter1 } from "@mui/icons-material";
import "../../../Css/filters.css";
import { ToolsIndices } from "../../../ToolsIndices";
export class GlitchFilter extends Component {
  state = {};
  glitchToolClickEvent = () => {    this.props.onClick(ToolsIndices.SubTools.GlitchFilter)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.glitchToolClickEvent}
      >
        <Filter1 className="glitch-filter" />
      </IconButton>
    );
  }
}
