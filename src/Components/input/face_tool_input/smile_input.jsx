import React, { Component } from "react";
import "../../../Css/input_area.css";
import { Slider, IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server } from "../../../Config";

export class SmileInput extends Component {
  state = {
    factor:5
  };

  SliderOnChange = (e) => {
    this.setState({ s: e.target.value });
  };

  postToServer = (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return;
    }
    const id = this.props.directoryID;
    const factor = this.state.factor;
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("Factor", factor);
    axios
      .post(Server + "/api-smile_tool", dataform, {
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
        <p className="factor-st">Factor: </p>
        <Slider
          defaultValue={5}
          color="secondary"
          valueLabelDisplay="auto"
          id="factor-slider"
          min={-50}
          max={50}
          onChange={this.SliderOnChange}
        />
        <p className="factor-value">Factor:{this.state.factor}</p>
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
