import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

class Home extends Component {
  componentDidMount() {
    let store = this.props.store.shopStore
    store.getShops()
  }
  render() {
    let store = this.props.store.shopStore
    let shopItems = store.shops.map(shop => (
      <h4 key={shop.id}>{shop.name}</h4>
    ))
    return (
      <div>
        {shopItems}
      </div>
    )
  }
}

export default inject('store')(observer(Home))