import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { Filter2 } from "@mui/icons-material";
import "../../../Css/filters.css";
import { ToolsIndices } from "../../../ToolsIndices";

export class CircleFilter extends Component {
  state = {};
  circleToolClickEvent = () => {    this.props.onClick(ToolsIndices.SubTools.CirclesFilter)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.circleToolClickEvent}
      >
        <Filter2 className="circle-filter" />
      </IconButton>
    );
  }
}
