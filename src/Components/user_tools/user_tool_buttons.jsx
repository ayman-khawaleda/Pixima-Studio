import React, { Component } from "react";
import { /*RedoButton,*/ UndoButton } from "./undo_redo";
import {
  Download_Button as DownloadButton,
  Upload_Button as UploadButton,
} from "./download_upload_buttons";
import { CompareButton } from "./compare";
import "bootstrap/dist/css/bootstrap.css";
import "../../Css/user-buttons.css";
import { ZoomButton } from "./zoom_tool";

export class UserTools extends Component {
  render() {
    return (
      <div className="user-tools">
        <ZoomButton onClick={this.props.onClick} />
        <CompareButton onClick={this.props.onClick} />
        <UndoButton
          onClick={this.props.onClick}
          ImageIndex={this.props.ImageIndex}
          setImageIndex={this.props.setImageIndex}
          setImageUrl={this.props.setImageUrl}
          DirectoryID={this.props.DirectoryID}
        />
        <DownloadButton url={this.props.ImageUrl} />
      </div>
    );
  }
}

export class UploadArea extends Component {
  render() {
    return <UploadButton {...this.props} />;
  }
}
