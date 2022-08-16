
import React, { Component } from "react";
import { BasicTools } from "./basic_tools";
import { FaceTools } from "./face_tools";
import "../../Css/main_tools.css";
import { BodyTool } from "./body_tool";
import { FiltersTool } from "./filters";

export class MainTools extends Component {
  state = { };
  toolsComponents = {
    basic_tools: <BasicTools onClick={this.props.onClick} setDefault={this.props.setDefault}/>,
    face_tools: <FaceTools onClick={this.props.onClick} setDefault={this.props.setDefault}/>,
    body_tool: <BodyTool onClick={this.props.onClick} setDefault={this.props.setDefault}/>,
    filters_tool: <FiltersTool onClick={this.props.onClick} setDefault={this.props.setDefault}/>,
  };
  render() {
    return (
      <div className="main-tools">
        <ul className="main-tools-list">
          <li>{this.toolsComponents.basic_tools}</li>
          <li>{this.toolsComponents.face_tools}</li>
          <li>{this.toolsComponents.body_tool}</li>
          <li>{this.toolsComponents.filters_tool}</li>
        </ul>
      </div>
    );
  }
}
