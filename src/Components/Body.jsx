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
    DefaultSubTool:7
  };
  setCurrentToolIndex = (index) => {
    this.setState({ Current: index });
  };
  setDefaultSubToolIndex = (index) => {
    this.setState({DefaultSubTool:index});
  }
  render() {
    return (
      <React.Fragment>
        <MainTools onClick={this.setCurrentToolIndex} setDefault={this.setDefaultSubToolIndex} />
        {/*<UploadArea />*/}
        <ImageArea />
        <UserTools onClick={this.setCurrentToolIndex}/>
        <SubTools tool_index={this.state.Current} sub_tool_default_index={this.state.DefaultSubTool}/>
      </React.Fragment>
    );
  }
}
