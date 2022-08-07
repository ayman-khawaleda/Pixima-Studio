import React, { Component } from "react";
import "../../../Css/input_area.css";
import { Slider, IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server, EndPoints } from "../../../Config";
import Select from "react-select";

export class CirclesFilterInput extends Component {
  state = {
    FaceKey: "RightEye",
    radius: 5,
  };
  FaceKeyOnChange = (e) => {
    this.setState({ FaceKey: e.value });
  };
  radiusSliderOnChange = (e) => {
    console.log(e)
    this.setState({ radius: e.target.value });
  };

  postToServer = (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return;
    }
    const id = this.props.directoryID;
    const { FaceKey,radius } = this.state;
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("FaceKey", FaceKey);
    dataform.append("Radius", radius);
    dataform.append("ImageIndex", 0);
    axios
      .post(Server + EndPoints.CirclesFilterToolEndPoint, dataform, {
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
  actions = [
    { label: "Right Eye", value: "RightEye" },
    { label: "Left Eye", value: "LeftEye" },
    { label: "Nose", value: "Nose" },
  ];
  render() {
    return (
      <React.Fragment>
        <Select
          aria-label={"FaceKey"}
          defaultMenuIsOpen
          className="select-list"
          options={this.actions}
          onChange={this.FaceKeyOnChange}
        />
        <p className="circle-radius-st">Radius: </p>
        <Slider
          defaultValue={5}
          color="secondary"
          valueLabelDisplay="auto"
          id="circle-radius-slider"
          min={5}
          max={30}
          onChange={this.radiusSliderOnChange}
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
