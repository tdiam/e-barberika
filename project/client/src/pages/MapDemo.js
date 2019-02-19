import React, { Component } from 'react'

import Map from '../components/Map'
import Marker from '../components/MapMarker'
import Overlay from '../components/MapOverlay'

class MapDemo extends Component {
    render() {
        return (
            <Map center={[0, 0]} zoom={3} width={600} height={400}>
                <Marker anchor={[54.13, 27.84]} />
                <Overlay anchor={[54.13, 1.321]}>Hello there</Overlay>
            </Map>
        )
    }
}

export default MapDemo