import React, { Component } from "react";
import { RedoButton, UndoButton } from "./undo_redo";
import {
  Download_Button as DownloadButton,
  Upload_Button as UploadButton,
} from "./download_upload_buttons";
import { CompareButton } from "./compare";
import "bootstrap/dist/css/bootstrap.css";
import "../../Css/user-buttons.css"

export class UserTools extends Component {
  render() {
    return (
      <div className="user-tools">
        <CompareButton onClick={this.props.onClick} />
        <UndoButton onClick={this.props.onClick} />
        <RedoButton onClick={this.props.onClick} />
        <DownloadButton />
      </div>
    );
  }
}

export class UploadArea extends Component {
  render() {
    return <UploadButton />;
  }
}
