import React, { Component } from "react";
import "../../Css/sub_tools.css";
import { ToolsIndices } from "../../ToolsIndices";
import { CropTool } from "../sub_tools/basic_tools/crop_tool";
import { ResizeTool } from "../sub_tools/basic_tools/resize";
import { SaturationTool } from "../sub_tools/basic_tools/saturation";
import { ContrastTool } from "../sub_tools/basic_tools/contrast";
import { FlipTool } from "../sub_tools/basic_tools/flip";
import { RotateTool } from "../sub_tools/basic_tools/rotate";
import { SmileTool } from "../sub_tools/face_tools/smile_tool";
import { GlitchFilter } from "./filters/glitch";
import { CircleFilter } from "./filters/circle";
import { ChangeClotheColor } from "./body_tools/change_color";
import { SmoothTool } from "./face_tools/smooth_tool";
import { ColorLipsTool } from "./face_tools/color_lips";
import { HairTool } from "./body_tools/hair_tool";
import { ColorEyeTool } from "./face_tools/color_eyes_tool";
import { NoseResizeTool } from "./face_tools/resize_nose_tool";
import { TeethTool } from "./face_tools/teeth_tool";
import { ResizeEyeTool } from "./face_tools/resize_eye_tool";
import { InputArea } from "../input/input_area";

export class SubTools extends Component {
  toolsIndices = [
    ToolsIndices.MainTool.BasicTools,
    ToolsIndices.MainTool.FaceTools,
    ToolsIndices.MainTool.BodyTools,
    ToolsIndices.MainTool.FilterTools,
  ];
  state = {
    sub_tool_index: 0,
  };
  tools = {};

  updateCurrentSubToolsEvent = (index) => {
    this.setState({ sub_tool_index: index });
  };

  constructor() {
    super();

    const { BasicTools, FaceTools, BodyTools, FilterTools } =
      ToolsIndices.MainTool;
    this.tools.last_tool_index = 0;
    this.tools.sub_tool_index = 7;
    this.tools[BasicTools] = [
      <FlipTool key={ToolsIndices.SubTools.FlipTool}onClick={this.updateCurrentSubToolsEvent} />,
      <RotateTool key={ToolsIndices.SubTools.RotateTool} onClick={this.updateCurrentSubToolsEvent} />,
      <CropTool key={ToolsIndices.SubTools.CropTool} onClick={this.updateCurrentSubToolsEvent} />,
      <ResizeTool key={ToolsIndices.SubTools.ResizeTool} onClick={this.updateCurrentSubToolsEvent} />,
      <ContrastTool key={ToolsIndices.SubTools.ContrastTool} onClick={this.updateCurrentSubToolsEvent} />,
      <SaturationTool key={ToolsIndices.SubTools.SaturationTool} onClick={this.updateCurrentSubToolsEvent} />,
    ];
    this.tools[FaceTools] = [
      <SmileTool key={ToolsIndices.SubTools.SmileTool} onClick={this.updateCurrentSubToolsEvent} />,
      <SmoothTool key={ToolsIndices.SubTools.SmoothFaceTool} onClick={this.updateCurrentSubToolsEvent} />,
      <ColorLipsTool key={ToolsIndices.SubTools.ColorLipsTool} onClick={this.updateCurrentSubToolsEvent} />,
      <ColorEyeTool key={ToolsIndices.SubTools.ColorEyeTool} onClick={this.updateCurrentSubToolsEvent} />,
      <ResizeEyeTool key={ToolsIndices.SubTools.ResizeEyeTool} onClick={this.updateCurrentSubToolsEvent} />,
      <NoseResizeTool key={ToolsIndices.SubTools.NoseResizeTool}onClick={this.updateCurrentSubToolsEvent} />,
      <TeethTool key={ToolsIndices.SubTools.WhiteTeethTool}onClick={this.updateCurrentSubToolsEvent} />,
    ];
    this.tools[BodyTools] = [
      <ChangeClotheColor
        key={ToolsIndices.SubTools.ChangeColorTool}
        onClick={this.updateCurrentSubToolsEvent}
      />,
      <HairTool
        key={ToolsIndices.SubTools.HairColorTool}
        onClick={this.updateCurrentSubToolsEvent}
      />,
    ];
    this.tools[FilterTools] = [
      <GlitchFilter
        key={ToolsIndices.SubTools.GlitchFilter}
        onClick={this.updateCurrentSubToolsEvent}
      />,
      <CircleFilter
        key={ToolsIndices.SubTools.CirclesFilter}
        onClick={this.updateCurrentSubToolsEvent}
      />,
    ];
  }

  render() {
    const { tool_index } = this.props;
    const res = this.toolsIndices.includes(tool_index);
    let block = 0;
    if (res) {
      block = this.tools[tool_index];
      this.tools.last_tool_index = tool_index;
    } else {
      block = this.tools[this.tools.last_tool_index];
    }
    return (
      <React.Fragment>
        <div className="sub-tools">
          {block.map((tool) => {
            return tool;
          })}
        </div>
        <InputArea
          tool_index={this.state.sub_tool_index}
          default_tool={this.tools.sub_tool_default_index}
        />
      </React.Fragment>
    );
  }
}
