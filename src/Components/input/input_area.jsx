import React, { Component } from "react";
import "../../Css/input_area.css";
import { ToolsIndices } from "../../ToolsIndices";
import { ColorHairInput } from "./body_tool_inputs/hair_input";
import { ColorEyesInput } from "./face_tool_input/color_eye_input";
import { ColorLipsInput } from "./face_tool_input/color_lips_input"
import { ResizeEyeInput } from "./face_tool_input/resize_eye_input";
import { ResizeNoseInput } from "./face_tool_input/resize_nose_input";
import { SmileInput } from "./face_tool_input/smile_input";
import { SmoothFaceInput } from "./face_tool_input/smooth_face_input";
import { WhiteTeethInput } from "./face_tool_input/white_teeth_input";
export class InputArea extends Component {
  state = {};

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
    if (this.props.tool_index === ToolsIndices.SubTools.EyeResizeTool) {
      return (
        <ResizeEyeInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
    if (this.props.tool_index === ToolsIndices.SubTools.NoseResizeTool) {
      return (
        <ResizeNoseInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
    if (this.props.tool_index === ToolsIndices.SubTools.WhiteTeethTool) {
      return (
        <WhiteTeethInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
    if (this.props.tool_index === ToolsIndices.SubTools.SmoothFaceTool) {
      return (
        <SmoothFaceInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
    if (this.props.tool_index === ToolsIndices.SubTools.HairColorTool) {
      return (
        <ColorHairInput
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
