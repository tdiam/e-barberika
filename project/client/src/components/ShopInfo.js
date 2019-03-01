import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { inject, observer } from 'mobx-react'

import Map from '../components/Map'
import Marker from '../components/MapMarker'
import Overlay from '../components/MapOverlay'

class ShopInfo extends Component {
  render () {
    const shop = this.props.shop
    const coords = [shop.lat, shop.lng]
    const tagList = shop.tags.map(tag => (
      <li>{ tag }</li>
    ))
    return (
      <div>
        <h2>Κατάστημα</h2>
        <h3>{ shop.name }</h3>
        <p>{ shop.address }</p>
        <p> Ετικέτες </p>
        <ul className='taglist'>
        { tagList }
        </ul>
        <Map center={coords}
        zoom={11}
        width={600} height={400}>
        <Marker anchor={coords} />
        <Overlay anchor={coords}>{ shop.name }</Overlay>
        </Map>
      </div>
    )
  }
}

ShopInfo.propTypes = {
  shop: PropTypes.object.isRequired,
}

export default inject('store')(observer(ShopInfo))
