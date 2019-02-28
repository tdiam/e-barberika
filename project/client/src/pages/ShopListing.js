import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

class ShopListing extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store.shopStore
  }
  componentDidMount () {
    // Execute API call that will update the store state
    this.store.getShops()
  }
  render () {
    let shopItems = this.store.shops.map(shop => (
      <li key={shop.id}>{ shop.name }</li>
    ))
    return (
      <div>
        <h2>Shops:</h2>
        <ul>
          { shopItems }
        </ul>
      </div>
    )
  }
}

export default inject('store')(observer(ShopListing))
