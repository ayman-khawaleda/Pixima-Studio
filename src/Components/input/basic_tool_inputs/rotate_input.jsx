import React, { Component } from "react";
import "../../../Css/input_area.css";
import { Slider, IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server, EndPoints } from "../../../Config";
import Select from "react-select";

export class RotateInput extends Component {
  state = {
    angle: 90,
    mode: "constant",
  };

  angleOnChange = (e) => {
    console.log("Angle: ",e.target.value);
    this.setState({ angle: e.target.value });
  };
  modeOnChange = (e) => {
    this.setState({ mode: e.value });
  };

  postToServer = async (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return;
    }
    const id = this.props.directoryID;
    const { angle, mode } = this.state;
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("Angle", angle);
    dataform.append("AreaMode", mode);
    await axios
      .post(Server + EndPoints.RotateToolEndPoint, dataform, {
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
  eadgeModes = [
    { label: "Constant", value: "constant" },
    { label: "Edge", value: "edge" },
    { label: "Reflect", value: "reflect" },
    { label: "Wrap", value: "wrap" },
  ];
  render() {
    return (
      <React.Fragment>
        <p className="rotate-st">Rotate: </p>
        <Slider
          color="secondary"
          valueLabelDisplay="auto"
          id="rotate-slider"
          min={0}
          max={360}
          onChange={this.angleOnChange}
        />
        <Select
          placeholder={"E-Modes"}
          className="select-list"
          options={this.eadgeModes}
          onChange={this.modeOnChange}
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
