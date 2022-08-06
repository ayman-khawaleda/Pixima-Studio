import React, { Component } from "react";
import "../../../Css/input_area.css";
import { Slider, IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import Hue from "@uiw/react-color-hue";
import axios from "axios";
import { Server } from "../../../Config";

export class ColorLipsInput extends Component {
  state = {
    h: 0,
    s: 0,
  };
  SliderOnChange = (e) => {
    this.setState({ s: e.target.value });
  };

  onChangeHue = (new_hue) => {
    this.setState({ ...new_hue });
  };

  postToServer = (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return
    }
    const id = this.props.directoryID;
    const color = [parseInt(this.state.h / 2)];
    const saturation = [this.state.s];
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("Color", color);
    dataform.append("Saturation", saturation);
    axios
      .post(Server + "/api-colorlips_tool", dataform, {
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
        <p className="hue-st">Hue: </p>
        <Hue onChange={this.onChangeHue} className="hue-picker" />
        <p className="saturation-st">Saturation: </p>
        <Slider
          defaultValue={0}
          color="secondary"
          valueLabelDisplay="auto"
          id="saturation-slider"
          min={0}
          max={100}
          onChange={this.SliderOnChange}
        />
        <p className="hue-value">Hue:{Math.floor(this.state.h)}</p>
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
