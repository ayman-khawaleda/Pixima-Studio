import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { Redo, Undo } from "@mui/icons-material";
import "../../Css/user-buttons.css"
import { ToolsIndices } from "../../ToolsIndices";

export class UndoButton extends Component {
  state = {

  };
  UndoOnClickEvent = e => {
    this.props.onClick(ToolsIndices.UserTool.UndoTool)
  }
  render() {
    return (
      
        <IconButton
          color="primary"
          component="label"
          onClick={this.UndoOnClickEvent}
        >
          <Undo className="undoIcon"/>
        </IconButton>
      
    );
  }
}

export class RedoButton extends Component {
  state = {};
  UndoOnClickEvent = () => {
    this.props.onClick(ToolsIndices.UserTool.RedoTool)
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.UndoOnClickEvent}
      >
        <Redo className="undoIcon" />
      </IconButton>
    );
  }
}
