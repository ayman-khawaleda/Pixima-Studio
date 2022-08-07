import React, { Component } from "react";
import "../../../Css/input_area.css";
import { Slider, IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server, EndPoints } from "../../../Config";

export class ContrastInput extends Component {
  state = {
    contrast: 50,
    brightness: 0,
  };
  contrastSliderOnChange = (e) => {
    this.setState({ contrast: e.target.value });
  };

  brightnessSliderOnChange = (e) => {
    this.setState({ brightness: e.target.value });
  };

  postToServer = (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return;
    }
    const id = this.props.directoryID;
    const { brightness, contrast } = this.state;
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("Contrast", contrast);
    dataform.append("Brightness", brightness);
    axios
      .post(Server + EndPoints.ContrastToolEndPoint, dataform, {
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

  render() {
    return (
      <React.Fragment>
        <p className="brightness-st">Contrast: </p>
        <Slider
          defaultValue={50}
          color="secondary"
          valueLabelDisplay="auto"
          id="contrast-slider"
          min={0}
          max={100}
          onChange={this.contrastSliderOnChange}
        />
        <p className="contrast-st">Brightness: </p>
        <Slider
          defaultValue={0}
          color="secondary"
          valueLabelDisplay="auto"
          id="brightness-slider"
          min={-100}
          max={100}
          onChange={this.brightnessSliderOnChange}
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
