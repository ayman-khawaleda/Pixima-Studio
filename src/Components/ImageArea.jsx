import { Construction } from "@mui/icons-material";
import React, { Component } from "react";
import "../Css/image_area.css";
import { ToolsIndices } from "../ToolsIndices";
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

  OnclickEvent = (ee) => {
    this.GetCoordinates(ee);
  };
  render() {
    if(this.props.currentActiveTool===ToolsIndices.UserTool.ZoomTool){
      console.log("Zoom Tool Clicked!! ")
    }
    return (
      <div className="image-area-div">
        <img
          src={require("../images/man.jpg")}
          id="image-area"
          alt=""
          onClick={(event) => {
            this.OnclickEvent(event);
          }}
        />
      </div>
    );
  }
}

export default ImageArea;
