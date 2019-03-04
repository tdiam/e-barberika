import React, { Component } from 'react'

/**
 * Pigeon maps passes to all children the props `left`, `top` in px.
 * See more: https://github.com/mariusandra/pigeon-maps/
 * Inspired by:
 * https://github.com/mariusandra/pigeon-marker/blob/master/src/index.js
 */
class MapMarker extends Component {
  render() {
    const { left, top, width, height, text } = this.props,
          offsetLeft = Math.floor(left - width / 2),
          offsetTop = top - height

    const style = {
      position: 'absolute',
      transform: `translate(${offsetLeft}px, ${offsetTop}px)`,
    }

    return (
      <div style={ style }>
        <img src="/img/pin.svg" alt="" width={ width } height={ height } />
        { text }
      </div>
    )
  }
}
MapMarker.defaultProps = {
  width: 32,
  height: 32,
  text: '',
}
 
export default MapMarker