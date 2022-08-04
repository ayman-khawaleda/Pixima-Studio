import React, { Component } from 'react';
import "../../Css/input_area.css"
import { Slider, IconButton } from '@mui/material';
import { AutoFixHigh } from '@mui/icons-material';
export class InputArea extends Component {
    state = {  } 
    render() { 
        return (
            <div className='input-area'>
            <Slider defaultValue={0}  color="secondary" valueLabelDisplay="auto" id="slider"/>
            <IconButton
            color="primary"
            component="label"
            onClick={null}
          >
            <AutoFixHigh className="check"/>
            </IconButton>
            </div>
        );
    }
}
