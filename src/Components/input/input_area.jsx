import React, { Component } from "react";
import "../../Css/input_area.css";
import { ToolsIndices } from "../../ToolsIndices";
import { ColorHairInput } from "./body_tool_inputs/hair_input";
import { ColorEyesInput } from "./face_tool_input/color_eye_input";
import { ColorLipsInput } from "./face_tool_input/color_lips_input";
import { ResizeEyeInput } from "./face_tool_input/resize_eye_input";
import { ResizeNoseInput } from "./face_tool_input/resize_nose_input";
import { SmileInput } from "./face_tool_input/smile_input";
import { SmoothFaceInput } from "./face_tool_input/smooth_face_input";
import { WhiteTeethInput } from "./face_tool_input/white_teeth_input";
import { ColorToolInput } from "./body_tool_inputs/color_tool_input";
import { GlitchFilterInput } from "./filters_tool_input/glitch_filter_input";
import { CirclesFilterInput } from "./filters_tool_input/circles_filter_input";
import { FlipInput } from "./basic_tool_inputs/flip_input";
import { ContrastInput } from "./basic_tool_inputs/contrast_input";
import { SaturationInput } from "./basic_tool_inputs/saturation_input";
export class InputArea extends Component {
  state = {};

  FactoryMethod() {
    if (this.props.tool_index === ToolsIndices.SubTools.EyeColorTool) {
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
    if (this.props.tool_index === ToolsIndices.SubTools.ChangeColorTool) {
      return (
        <ColorToolInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
          lastMouseClick={this.props.lastClick}
        />
      );
    }
    if (this.props.tool_index === ToolsIndices.SubTools.GlitchFilter) {
      return (
        <GlitchFilterInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
    if (this.props.tool_index === ToolsIndices.SubTools.CirclesFilter) {
      return (
        <CirclesFilterInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
    if (this.props.tool_index === ToolsIndices.SubTools.FlipTool) {
      return (
        <FlipInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
    if (this.props.tool_index === ToolsIndices.SubTools.ContrastTool) {
      return (
        <ContrastInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
    if (this.props.tool_index === ToolsIndices.SubTools.SaturationTool) {
      return (
        <SaturationInput
          setImageUrl={this.props.setImageUrl}
          hasImage={this.props.hasImage}
          directoryID={this.props.directoryID}
          ImageIndex={this.props.ImageIndex}
        />
      );
    }
  }
  render() {
    return <div className="input-area">{this.FactoryMethod()}</div>;
  }
}
