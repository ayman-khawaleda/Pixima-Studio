import React, { Component } from "react";
import "../../../Css/input_area.css";
import { IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server, EndPoints } from "../../../Config";

export class ResizeInput extends Component {
  state = {
    newWidth: 0,
    newHeight: 0,
  };
  widthOnChange = (e) => {
    this.setState({ newWidth: e.target.value });
  };
  heightOnChange = (e) => {
    this.setState({ newHeight: e.target.value });
  };

  postToServer = async (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return;
    }
    const id = this.props.directoryID;
    var { newHeight,newWidth } = this.state;
    try{
        newHeight = parseInt(newHeight)
        newWidth = parseInt(newWidth)
    }catch(error){
        alert("Error In Resize Input")
        return
    }
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("Width", newWidth);
    dataform.append("High", newHeight);
    await axios
      .post(Server + EndPoints.ResizeToolEndPoint, dataform, {
        "Content-Type": "multipart/form-data",
      })
      .then((respones) => {
        if (respones.data.code === 200) {
          const image_url = respones.data.Image;
          // const image_preview = respones.data.ImagePreview
          // const image_mask = respones.data.Mask
          this.props.setImageUrl(image_url);
        } else {
          alert("Error In Inputs")
        }
      })
      .catch((error) => {
        console.log(error);
      });
    // dataform.append("ImageIndex",ImageIndex)
  };

  render() {
    return (
      <React.Fragment>
        <input
          placeholder="Width"
          required={true}
          id="width-text"
          onChange={this.widthOnChange}
        />
        <input
          placeholder="Hieght"
          required={true}
          id="height-text"
          onChange={this.heightOnChange}
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
