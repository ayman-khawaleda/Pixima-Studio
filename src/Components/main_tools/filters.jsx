import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { Filter as FilterIcon } from "@mui/icons-material";
import "../../Css/main_tools.css";
import { ToolsIndices } from "../../ToolsIndices";
export class FiltersTool extends Component {
  state = {};
  filtersToolClickEvent = () => {
    this.props.onClick(ToolsIndices.MainTool.FilterTools);
    this.props.setDefault(ToolsIndices.SubTools.CirclesFilter)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.filtersToolClickEvent}
      >
        <FilterIcon className="filters-tools" />
      </IconButton>
    );
  }
}
