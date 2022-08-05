import React, { Component } from "react";
import {
  UserTools,
  UploadArea,
} from "../Components/user_tools/user_tool_buttons";
import { MainTools } from "../Components/main_tools/main_tool_button";
import { SubTools } from "./sub_tools/sub_tool_buttons.jsx";
import ImageArea from "./ImageArea";
import "../Css/index.css"
export class Body extends Component {
  state = {
    CurrentIndex: 0,
    DefaultSubTool: 7,
    hasImage: true,
  };
  setCurrentToolIndex = (index) => {
    this.setState({ CurrentIndex: index });
  };
  setDefaultSubToolIndex = (index) => {
    this.setState({ DefaultSubTool: index });
  };

  setHasImage = (hasImage) => {
    this.setState({ hasImage });
  };
  render() {
    const imageBlock = this.state.hasImage ? (
      <ImageArea currentActiveTool={this.state.CurrentIndex} />
    ) : (
      <UploadArea setHasImage={this.setHasImage} />
    );
    return (
      <React.Fragment>
        <MainTools
          onClick={this.setCurrentToolIndex}
          setDefault={this.setDefaultSubToolIndex}
        />
        {imageBlock}
        <UserTools onClick={this.setCurrentToolIndex} />
        <SubTools
          tool_index={this.state.CurrentIndex}
          sub_tool_default_index={this.state.DefaultSubTool}
        />
      </React.Fragment>
    );
  }
}
