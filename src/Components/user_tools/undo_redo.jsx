import React, { Component } from "react";
import IconButton from "@mui/material/IconButton";
import { Redo, Undo } from "@mui/icons-material";
import "../../Css/user-buttons.css";
import { ToolsIndices } from "../../ToolsIndices";
import axios from "axios";
import { Server } from "../../Config";
export class UndoButton extends Component {
  state = {};
  UndoOnClickEvent = async (e) => {
    // this.props.onClick(ToolsIndices.UserTool.UndoTool);
    const formdata = new FormData();
    formdata.append("id", this.props.DirectoryID);
    await axios
      .delete(Server + "/api-images", {
        data: formdata,
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((res) => {
        if (res.data.code === 200) {
          this.props.setImageUrl(res.data.Image)
        }
      })
      .catch((e) => console.log(e));
  };
  render() {
    return (
      <IconButton
        color="primary"
        component="label"
        onClick={this.UndoOnClickEvent}
      >
        <Undo className="undoIcon" />
      </IconButton>
    );
  }
}

export class RedoButton extends Component {
  state = {};
  UndoOnClickEvent = () => {
    this.props.onClick(ToolsIndices.UserTool.RedoTool);
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
