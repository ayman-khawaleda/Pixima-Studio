import React, { Component } from "react";
import "../../Css/user-buttons.css";
import IconButton from "@mui/material/IconButton";
import { Download, Upload } from "@mui/icons-material";
import axios from "axios";

export class Download_Button extends Component {
  state = {
    url: "",
  };
  download_action = (e) => {
    var ImageName = window.prompt("Enter Image Name", "Image.jpg");
    try {
      if (ImageName.slice(-3) !== "jpg") {
        ImageName += "jpg";
      }
    } catch (Excepation) {
      ImageName = "Image.jpg";
    }
    const { url } = this.state;
    const full_url = "http://localhost:8000/" + url;
    axios({
      url: full_url,
      method: "GET",
      responseType: "blob",
    })
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", { ImageName });
        document.body.appendChild(link);
        link.click();
      })
      .catch((err) => console.log(err));
  };

  render() {
    return (
      <React.Fragment>
        <IconButton
          color="primary"
          component="label"
          onClick={this.download_action}
        >
          <Download className="donwloadIcon" />
        </IconButton>
      </React.Fragment>
    );
  }
}

export class Upload_Button extends Component {
  state = {};

  render() {
    return (
      <IconButton
        color="primary"
        aria-label="upload picture"
        component="label"
        className="upload-btn"
      >
        <div className="upload-area">
          <p className="upload-st">Upload Image</p>
          <input hidden accept="image/*" type="file" />
          <Upload className="uploadIcon" />
        </div>
      </IconButton>
    );
  }
}
