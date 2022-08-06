import React, { Component } from "react";
import "../../Css/input_area.css";
import { ToolsIndices } from "../../ToolsIndices";
import { ColorEyesInput } from "./face_tool_input/color_eye_input";
import { ColorLipsInput } from "./face_tool_input/color_lips_input"
import { SmileInput } from "./face_tool_input/smile_input";
export class InputArea extends Component {
  state = {};

  SliderOnChange = (e) => {
    console.log("Slider: ", e.target.value);
  };
  
  FactoryMethod(){
    if(this.props.tool_index===ToolsIndices.SubTools.EyeColorTool){
      return (
        <ColorEyesInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
    if (this.props.tool_index === ToolsIndices.SubTools.ColorLipsTool) {
      return (
        <ColorLipsInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
    if (this.props.tool_index === ToolsIndices.SubTools.SmileTool) {
      return (
        <SmileInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
  }
  render() {
    return (
      <div className="input-area">
        {this.FactoryMethod()}
      </div>
    );
  }
}
