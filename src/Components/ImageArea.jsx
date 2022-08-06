import React, { Component } from "react";
import {
  TransformComponent,
  TransformWrapper,
} from "@pronestor/react-zoom-pan-pinch";
import "../Css/image_area.css";
import { ToolsIndices } from "../ToolsIndices";
import { ReactCompareImageSlider } from "react-compare-image-slider";

class ImageArea extends Component {
  state = {
    oldestClick: [0, 0],
    lastClick: [0, 0],
  };

  FindPosition(oElement) {
    if (typeof oElement.offsetParent != "undefined") {
      for (var posX = 0, posY = 0; oElement; oElement = oElement.offsetParent) {
        posX += oElement.offsetLeft;
        posY += oElement.offsetTop;
      }
      return [posX, posY];
    } else {
      return [oElement.x, oElement.y];
    }
  }

  GetCoordinates(e) {
    var PosX = 0;
    var PosY = 0;
    var ImgPos;
    var ele = document.getElementById("image-area");
    let { width, height, naturalWidth, naturalHeight } = ele;
    ImgPos = this.FindPosition(ele);
    let widthRatio = width / naturalWidth;
    let heightRatio = height / naturalHeight;

    if (e.pageX || e.pageY) {
      PosX = e.pageX;
      PosY = e.pageY;
    } else if (e.clientX || e.clientY) {
      PosX =
        e.clientX +
        document.body.scrollLeft +
        document.documentElement.scrollLeft;
      PosY =
        e.clientY +
        document.body.scrollTop +
        document.documentElement.scrollTop;
    }
    PosX = PosX - ImgPos[0];
    PosY = PosY - ImgPos[1];
    this.setState({
      oldestClick: this.state.lastClick,
      lastClick: [PosX * (1 / widthRatio), PosY * (1 / heightRatio)].map(
        (num) => Math.trunc(num)
      ),
    });
  }

  OnclickEvent = (e) => {
    this.GetCoordinates(e);
    const {oldestClick,lastClick} = this.state
    this.props.setMouseClicks(oldestClick,lastClick);
  };


  render() {
    let image_block = 0;
    if (this.props.currentActiveTool === ToolsIndices.UserTool.CompareTool) {
      image_block = (
        <ReactCompareImageSlider
          leftImage={this.props.firstImageUrl}
          rightImage={this.props.lastImageUrl}
        />
      );
    } else if (
      this.props.currentActiveTool === ToolsIndices.UserTool.ZoomTool
    ) {
      image_block = (
        <TransformWrapper>
          <TransformComponent>
            <img
              src={this.props.lastImageUrl}
              id="image-area"
              alt="CurrentImage"
            />
          </TransformComponent>
        </TransformWrapper>
      );
    } else {
      image_block = (
        <img
          src={this.props.lastImageUrl}
          id="image-area"
          alt="CurrentImage"
          onClick={this.OnclickEvent}
        />
      );
    }
    return <div className="image-area-div">{image_block}</div>;
  }
}

export default ImageArea;
