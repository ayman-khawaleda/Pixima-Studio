import React, { Component } from "react";
import {
  UserTools,
  UploadArea,
} from "../Components/user_tools/user_tool_buttons";
import { MainTools } from "../Components/main_tools/main_tool_button";
import { SubTools } from "./sub_tools/sub_tool_buttons.jsx";
import ImageArea from "./ImageArea";
import "../Css/index.css";
import { Server } from "../Config.js";
export class Body extends Component {
  state = {
    CurrentIndex: 0,
    DefaultSubTool: 7,
    HasImage: false,
    CurrentUrl: "",
    DirectoryID: "",
    CurrentImageIndex: -1,
    firstImageUrl: "",
    lastImageUrl: "",
    firstUpload: true,
    oldClick: [0, 0],
    lastClick: [0, 0],
  };
  setCurrentToolIndex = (index) => {
    this.setState({ CurrentIndex: index });
  };

  setDefaultSubToolIndex = (index) => {
    this.setState({ DefaultSubTool: index });
  };

  setHasImageEvent = (hasImage) => {
    this.setState({ HasImage: hasImage });
  };

  setImageUrl = (url) => {
    this.setState({ CurrentUrl: url });
    this.getImage(url);
  };

  setDirectoryID = (id) => {
    this.setState({ DirectoryID: id });
  };
  setCurrentImageIndex = (index) => {
    this.setState({ CurrentImageIndex: index });
  };

  getImage(url) {
    try {
      if (this.state.firstUpload) {
        this.setState({
          firstImageUrl: Server + url,
          lastImageUrl: Server + url,
          firstUpload: false,
          CurrentImageIndex:0
        });
      } else {
        this.setState({
          lastImageUrl: Server + url,
          CurrentImageIndex:this.state.CurrentImageIndex+1
        });
      }
    } catch (error) {
      alert("Error Code During Fetching Data...ImageArea");
    }
  }
  setMouseClicks = (oldClick, lastClick) => {
    // console.log(oldClick,lastClick)
    this.setState({
      oldClick, 
      lastClick,
    });
  };
  render() {
    const imageBlock = this.state.HasImage ? (
      <ImageArea
        currentActiveTool={this.state.CurrentIndex}
        firstImageUrl={this.state.firstImageUrl}
        lastImageUrl={this.state.lastImageUrl}
        setMouseClicks={this.setMouseClicks}
      />
    ) : (
      <UploadArea
        setHasImage={this.setHasImageEvent}
        setImageUrl={this.setImageUrl}
        setDirectoryID={this.setDirectoryID}
        setCurrentImageIndex={this.setCurrentImageIndex}
      />
    );
    return (
      <React.Fragment>
        <MainTools
          onClick={this.setCurrentToolIndex}
          setDefault={this.setDefaultSubToolIndex}
        />
        {imageBlock}
        <UserTools
          onClick={this.setCurrentToolIndex}
          ImageUrl={this.state.lastImageUrl}
          setImageUrl={this.setImageUrl}
          ImageIndex={this.state.CurrentImageIndex}
          setImageIndex={this.setCurrentImageIndex}
          DirectoryID={this.state.DirectoryID}
        />
        <SubTools
          tool_index={this.state.CurrentIndex}
          setImageUrl={this.setImageUrl}
          setCurrentImageIndex={this.setCurrentImageIndex}
          oldClick={this.state.oldClick}
          lastClick={this.state.lastClick}
          hasImage={this.state.HasImage}
          directoryID={this.state.DirectoryID}
          ImageIndex={this.state.CurrentImageIndex}
        />
      </React.Fragment>
    );
  }
}
