import React, { Component } from "react";
import "../../../Css/input_area.css";
import { IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server, EndPoints } from "../../../Config";
import Select from "react-select";

export class CropInput extends Component {
  state = {
    Ratio: "1:1",
  };

  ratioOnChange = (e) => {
    this.setState({ Ratio: e.value });
  };

  postToServer = async (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return;
    }
    const id = this.props.directoryID;
    var { Ratio } = this.state;
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("Ratio", Ratio);
    await axios
      .post(Server + EndPoints.CropToolEndPoint, dataform, {
        "Content-Type": "multipart/form-data",
      })
      .then((respones) => {
        if (respones.data.code === 200) {
          const image_url = respones.data.Image;
          // const image_preview = respones.data.ImagePreview
          // const image_mask = respones.data.Mask
          this.props.setImageUrl(image_url);
        } else {
          alert("Error In Inputs");
          console.log(respones);
        }
      })
      .catch((error) => {
        console.log(error);
      });
    // dataform.append("ImageIndex",ImageIndex)
  };
  actions = [
    { label: "1:1", value: "1:1" },
    { label: "4:3", value: "4:3" },
    { label: "5:4", value: "5:4" },
    { label: "9:16", value: "9:16" },
    { label: "16:9", value: "16:9" },
  ];
  render() {
    return (
      <React.Fragment>
        <Select
          defaultMenuIsOpen
          className="ratio-select-list"
          options={this.actions}
          onChange={this.ratioOnChange}
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
