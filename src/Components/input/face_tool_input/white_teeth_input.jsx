import React, { Component } from "react";
import "../../../Css/input_area.css";
import { Slider, IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server,EndPoints } from "../../../Config";

export class WhiteTeethInput extends Component {
  state = {
    saturation: 40,
    brightness: 20,
  };

  saturationSliderOnChange = (e) => {
    this.setState({ saturation: e.target.value });
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
    const { saturation, brightness } = this.state;
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("Saturation", saturation);
    dataform.append("Brightness", brightness);
    axios
      .post(Server + EndPoints.WhiteTeethToolEndPoint, dataform, {
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
        <p className="teeth-saturation-st">Saturation</p>
        <Slider
          defaultValue={40}
          color="secondary"
          valueLabelDisplay="auto"
          id="teeth-saturation-slider"
          min={0}
          max={255}
          onChange={this.saturationSliderOnChange}
        />
        <p className="teeth-saturation-value">
          Saturation:{this.state.saturation}
        </p>
        <p className="brightness-st">Brightness</p>
        <Slider
          defaultValue={20}
          color="secondary"
          valueLabelDisplay="auto"
          id="brightness-slider"
          min={0}
          max={255}
          onChange={this.brightnessSliderOnChange}
        />
        <p className="brightness-value">Brightness:{this.state.brightness}</p>
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
