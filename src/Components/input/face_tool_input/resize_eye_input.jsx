import React, { Component } from "react";
import "../../../Css/input_area.css";
import { Slider, IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server } from "../../../Config";

export class ResizeEyeInput extends Component {
  state = {
    factor: 1.1,
    radius: 75,
  };

  SliderOnChange = (e) => {
    this.setState({ factor: e.target.value });
  };
  radiusSliderOnChange = (e) => {
    this.setState({ radius: e.target.value });
  };

  postToServer = (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return;
    }
    const id = this.props.directoryID;
    const {radius,factor} = this.state;
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("Factor", factor);
    dataform.append("Radius",radius);
    axios
      .post(Server + "/api-resizeeyes_tool", dataform, {
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
        <p className="factor-st">Factor</p>
        <Slider
          defaultValue={1.1}
          color="secondary"
          valueLabelDisplay="auto"
          id="factor-slider"
          min={0.75}
          max={2}
          step={0.01}
          onChange={this.SliderOnChange}
        />
        <p className="factor-value">Factor:{this.state.factor}</p>
        <p className="radius-st">Radius</p>
        <Slider
          defaultValue={75}
          color="secondary"
          valueLabelDisplay="auto"
          id="radius-slider"
          min={50}
          max={200}
          onChange={this.radiusSliderOnChange}
        />
        <p className="radius-value">Radius:{this.state.radius}</p>
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
