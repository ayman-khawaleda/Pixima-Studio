import React, { Component } from "react";
import {
  UserTools,
  UploadArea,
} from "../Components/user_tools/user_tool_buttons";
import { MainTools } from "../Components/main_tools/main_tool_button";
import { SubTools } from "./sub_tools/sub_tool_buttons.jsx";
import ImageArea from "./ImageArea";

export class Body extends Component {
  state = {
    Current: 0,
    DefaultSubTool: 7,
    hasImage: true,
  };
  setCurrentToolIndex = (index) => {
    this.setState({ Current: index });
  };
  setDefaultSubToolIndex = (index) => {
    this.setState({ DefaultSubTool: index });
  };

  setHasImage = (hasImage) => {
    this.setState({ hasImage })
  }
  render() {
    const imageBlock = this.state.hasImage ? <ImageArea /> : <UploadArea setHasImage={this.setHasImage}/>;
    return (
      <React.Fragment>
        <MainTools
          onClick={this.setCurrentToolIndex}
          setDefault={this.setDefaultSubToolIndex}
        />
        {imageBlock}
        <UserTools onClick={this.setCurrentToolIndex} />
        <SubTools
          tool_index={this.state.Current}
          sub_tool_default_index={this.state.DefaultSubTool}
        />
      </React.Fragment>
    );
  }
}
