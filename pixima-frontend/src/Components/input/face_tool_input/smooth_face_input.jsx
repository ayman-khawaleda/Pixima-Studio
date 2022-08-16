import React, { Component } from "react";
import "../../../Css/input_area.css";
import { Slider, IconButton } from "@mui/material";
import { AutoFixHigh } from "@mui/icons-material";
import axios from "axios";
import { Server , EndPoints} from "../../../Config";

export class SmoothFaceInput extends Component {
  state = {
    kernal: 5,
    factor: 50,
  };

  kernalSliderOnChange = (e) => {
    this.setState({ kernal: e.target.value });
  };
  factorSliderOnChange = (e) => {
    this.setState({ factor: e.target.value });
  };

  postToServer = async (e) => {
    if (!this.props.hasImage) {
      alert("Image Required");
      return;
    }
    const id = this.props.directoryID;
    const { kernal, factor } = this.state;
    // const ImageIndex = this.props.ImageIndex
    const dataform = new FormData();
    dataform.append("id", id);
    dataform.append("SigmaX", factor);
    dataform.append("SigmaY", factor);
    dataform.append("Kernal", kernal);
    await axios
      .post(Server + EndPoints.SmoothFaceToolEndPoint, dataform, {
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
          defaultValue={50}
          color="secondary"
          valueLabelDisplay="auto"
          id="factor-slider"
          min={0}
          max={150}
          onChange={this.factorSliderOnChange}
        />
        <p className="factor-value">
          Factor:{this.state.factor}
        </p>
        <p className="kernal-st">Kernal</p>
        <Slider
          defaultValue={5}
          color="secondary"
          valueLabelDisplay="auto"
          id="kernal-slider"
          min={3}
          max={31}
          step={2}
          onChange={this.kernalSliderOnChange}
        />
        <p className="kernal-value">Kernal:{this.state.kernal}</p>
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
