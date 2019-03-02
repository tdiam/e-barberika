import React, { Component } from 'react'
import { FormGroup, Label, Input } from 'reactstrap'

import Map from '../Map'
import Draggable from '../MapDraggable'


class GeoFilter extends Component {
  constructor (props) {
    super(props)
    this.prepareData()
  }
  state = {
    geoDist: '',
    geoLat: '',
    geoLng: '',
  }
  changeHandler = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    })
  }
  /**
   * Prepare data for parent.
   * If at least one but not all is unset, set all to undefined and send error.
   */
  prepareData () {
    let { geoDist, geoLat, geoLng } = this.state
    // store them in array for easy access
    let check = [geoDist, geoLat, geoLng]
    // count how many of them are unset
    let numOfUnset = check.filter(v => v === '').length
    let geoError = ''
    // if at least one but not all are unset, it's an error and set them to undefined
    if (numOfUnset > 0 && numOfUnset < check.length) {
      geoDist = geoLat = geoLng = ''
      geoError = 'Για χρήση του φίλτρου απόστασης πρέπει να επιλέξετε απόσταση και σημείο στον χάρτη.'
    }
    this.props.onPrepared({ geoDist, geoLat, geoLng, geoError })
  }
  componentDidUpdate (_prevProps, prevState) {
    if (this.state.geoDist !== prevState.geoDist
     || this.state.geoLat !== prevState.geoLat
     || this.state.geoLng !== prevState.geoLng
    ) {
      this.prepareData()
    }
  }
  render() {
    const { geoLat, geoLng, geoDist } = this.state 
    return (
      <FormGroup>
        <Map center={[0, 0]} zoom={3} width={600} height={400}>
          <Draggable
            anchor={[geoLat, geoLng]}
            onDragEnd={ ([lat, lng]) => this.setState({ geoLat: lat, geoLng: lng }) }
          >
            <img src="img/pin.svg" alt="Επιλογή τοποθεσίας" width="32" height="32" />
          </Draggable>
        </Map>
        <Label htmlFor="geoDist">Απόσταση</Label>
        <Input
          type="number"
          name="geoDist"
          value={ geoDist }
          onChange={ this.changeHandler }
          step="1" min="1"
          ></Input>
      </FormGroup>
    )
  }
}
 
export default GeoFilter