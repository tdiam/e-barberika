import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

import StateHandler from '../components/StateHandler'
import Map from '../components/Map'
import Marker from '../components/MapMarker'
import Overlay from '../components/MapOverlay'

class Shop extends Component {
  constructor (props) {
    super(props)
    this.store = props.store.shopStore
  }
  componentDidMount () {
    // Fetch shop with given ID
    this.store.getShop(this.props.match.params.id)
  }
  render () {
    const { shop, state } = this.store
    return (
      <StateHandler state={state}>
        { /* This will be rendered only if state is 'done'.
             See StateHandler source for more info.
             The component must also be returned from a function
             and not directly to avoid 'x is undefined' errors. */
        }
        {() => {
          const coords = [shop.lat, shop.lng]
          const tagList = shop.tags.map(tag => (
            <li>{ tag }</li>
          ))
          return (
            <div>
              <h3>{ shop.name }</h3>
              <p>{ shop.address }</p>
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
        }}
      </StateHandler>
    )
  }
}

export default inject('store')(observer(Shop))
