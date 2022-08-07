import React, { Component } from "react";
import "../../../Css/input_area.css";
import { IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server, EndPoints } from "../../../Config";
import Select from "react-select";

export class FlipInput extends Component {
  state = {
    dir: "Hor",
  };
  DirectionOnChange = (e) => {
    this.setState({ dir: e.value });
  };

  postToServer = (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return;
    }
    const id = this.props.directoryID;
    const { dir } = this.state;
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("Direction", dir);
    axios
      .post(Server + EndPoints.FlipToolEndPoint, dataform, {
        "Content-Type": "multipart/form-data",
      })
      .then((respones) => {
        if (respones.data.code === 200) {
          const image_url = respones.data.Image;
          // const image_preview = respones.data.ImagePreview
          // const image_mask = respones.data.Mask
          this.props.setImageUrl(image_url);
        } else {
          console.log(respones);
        }
      })
      .catch((error) => {
        console.log(error);
      });
    // dataform.append("ImageIndex",ImageIndex)
  };
  actions = [
    { label: "Horizontal", value: "Hor" },
    { label: "Vertical", value: "Ver" },
  ];
  render() {
    return (
      <React.Fragment>
        <Select
          defaultMenuIsOpen
          className="select-list"
          options={this.actions}
          onChange={this.DirectionOnChange}
        />
        <IconButton
          color="primary"
          component="label"
          onClick={this.postToServer}
        >
          <AutoFixHigh className="check" />
        </IconButton>
      </React.Fragment>
    );
  }
}
