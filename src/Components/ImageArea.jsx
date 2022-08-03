import React, { Component } from 'react'
import "../Css/image_area.css"
class ImageArea extends Component {
    state = {  } 
    render() { 
        return (
            <div className="image-area-div">
                <img src= {require("../images/man.jpg")} className="image-area" alt="" />
            </div>
        );
    }
}

export default ImageArea;