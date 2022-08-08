import React, { Component } from "react";
import "../../../Css/input_area.css";
import { Slider, IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server, EndPoints } from "../../../Config";

export class GlitchFilterInput extends Component {
  state = {
    shift: 20,
    step: 15,
    density: 5,
  };
  shiftSliderOnChange = (e) => {
    this.setState({ shift: e.target.value });
  };

  stepSlideronChange = (e) => {
    this.setState({ step: e.target.value });
  };

  densitySlideronChange = (e) => {
    this.setState({ density: e.target.value });
  };

  postToServer = async (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return;
    }
    const id = this.props.directoryID;
    const {step,shift,density} = this.state
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("Step", step);
    dataform.append("Shift", shift);
    dataform.append("Density",density)
    // dataform.append("ImageIndex", 0);
    await axios
      .post(Server + EndPoints.GlitchFilterToolEndPoint, dataform, {
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
        <p className="shift-st">Shift: </p>
        <Slider
          defaultValue={5}
          color="secondary"
          valueLabelDisplay="auto"
          id="shift-slider"
          min={5}
          max={50}
          onChange={this.shiftSliderOnChange}
        />
        <p className="step-st">Step: </p>
        <Slider
          defaultValue={5}
          color="secondary"
          valueLabelDisplay="auto"
          id="step-slider"
          min={5}
          max={25}
          onChange={this.stepSlideronChange}
        />
        <p className="density-st">Density: </p>
        <Slider
          defaultValue={0}
          color="secondary"
          valueLabelDisplay="auto"
          id="density-slider"
          min={0}
          max={50}
          onChange={this.densitySlideronChange}
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
