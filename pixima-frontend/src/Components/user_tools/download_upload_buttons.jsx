import React, { Component } from "react";
import "../../Css/user-buttons.css";
import IconButton from "@mui/material/IconButton";
import { Download, Upload } from "@mui/icons-material";
import axios from "axios";
import { Server } from "../../Config";
export class Download_Button extends Component {
  state = {};
  download_action = (e) => {
    var ImageName = window.prompt("Enter Image Name", "Image.jpg");
    try {
      if (ImageName.slice(-3) !== "jpg") {
        ImageName += ".jpg";
      }
    } catch (Excepation) {
      ImageName = "Image.jpg";
    }
    this.getImage(this.props.url, ImageName);
  };
  getImage(url, ImageName) {
    try {
      axios.get(url, { responseType: "blob" }).then((res) => {
        const blob = URL.createObjectURL(
          new Blob([res.data], { type: "image/jpg" })
        );
        const link = document.createElement("a");
        link.href = blob;
        link.download = ImageName;
        document.body.appendChild(link);
        link.click();
      });
    } catch (error) {
      console.log(error);
    }
  }
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
  accepted_ext = ["jpg", "png"];
  onChangeEvent = (e) => {
    const file = e.target.files[0];
    const ext = file.name.slice(-3);
    if (!this.accepted_ext.includes(ext)) {
      alert("Enter Jpg/Png File");
      return;
    }
    const form = new FormData();
    form.append("Image", file);
    this.uploadImage2API(form);
  };
  async uploadImage2API(form) {
    try {
      const response = await axios.post(Server + "/api-upload_image", form, {
        "Content-Type": "multipart/form-data",
      });
      if (response.data.code === 200) {
        this.props.setHasImage(true);
        this.props.setImageUrl(response.data.Image);
        this.props.setDirectoryID(response.data.id);
        this.props.setCurrentImageIndex(0);
      } else {
        alert("Error In Upload");
      }
    } catch (error) {
      alert("Error Code In Upload");
    }
  }

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
          <input
            hidden
            accept="image/*.jpg"
            type="file"
            id="upload-image"
            onChange={this.onChangeEvent}
          />
          <Upload className="uploadIcon" />
        </div>
      </IconButton>
    );
  }
}
