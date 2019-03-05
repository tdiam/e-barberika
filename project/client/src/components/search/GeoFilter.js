import React, { Component } from 'react'
import { FormGroup, Button, Label, Input } from 'reactstrap'

import Map from '../Map'
import Draggable from '../MapDraggable'


class GeoFilter extends Component {
  constructor (props) {
    super(props)
    this.prepareData()
  }
  state = {
    geoDist: '',
    geoLat: 38.008928,
    geoLng: 23.747025,
    pinActive: false,
  }
  changeHandler = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    })
  }
  togglePin = () => {
    this.setState(prevState => ({
      pinActive: !prevState.pinActive,
    }))
  }
  /**
   * Prepare data for parent.
   * If at least one but not all is unset, set all to undefined and send error.
   */
  prepareData () {
    let { geoDist, geoLat, geoLng, pinActive } = this.state
    if (!pinActive) {
      geoLat = geoLng = ''
    }
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
     || this.state.pinActive !== prevState.pinActive
    ) {
      this.prepareData()
    }
  }
  render() {
    const { geoLat, geoLng, geoDist, pinActive } = this.state 
    return (
      <>
        <FormGroup>
          <Map center={[38.008928, 23.747025]} zoom={ 4 } height={ 400 }>
            <Draggable
              anchor={[geoLat, geoLng]}
              offset={[16, 32]}
              onDragEnd={ ([lat, lng]) => this.setState({ geoLat: lat, geoLng: lng }) }
            >
              <img
                className={ !pinActive && "inactive" }
                src="/img/pin.svg"
                alt="Επιλογή τοποθεσίας"
                width="32" height="32" />
            </Draggable>
          </Map>
          <Button size="sm" onClick={ this.togglePin } active={ pinActive }>
            Τοποθεσία: { pinActive ? 'Ενεργή' : 'Ανενεργή' }
          </Button>
        </FormGroup>
        <FormGroup>
          <Label htmlFor="geoDist">Απόσταση</Label>
          <Input
            type="number"
            name="geoDist"
            value={ geoDist }
            onChange={ this.changeHandler }
            step="1" min="1"
            ></Input>
        </FormGroup>
      </>
    )
  }
}
 
export default GeoFilter