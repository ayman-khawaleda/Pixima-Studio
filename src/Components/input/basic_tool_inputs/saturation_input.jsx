import React, { Component } from "react";
import "../../../Css/input_area.css";
import { Slider, IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server, EndPoints } from "../../../Config";

export class SaturationInput extends Component {
  state = {
    saturation: 0,
  };
  SliderOnChange = (e) => {
    this.setState({ saturation: e.target.value });
  };

  postToServer = async (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return;
    }
    const id = this.props.directoryID;
    const { saturation } = this.state;
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("Saturation", saturation);
    await axios
      .post(Server + EndPoints.SaturationToolEndPoint, dataform, {
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
        <p className="saturation-st">Saturation: </p>
        <Slider
          defaultValue={50}
          color="secondary"
          valueLabelDisplay="auto"
          id="saturation-tool-slider"
          min={0}
          max={100}
          onChange={this.SliderOnChange}
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
