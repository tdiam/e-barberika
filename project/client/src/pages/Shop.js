import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

import StateHandler from '../components/StateHandler'

import ShopInfo from '../components/ShopInfo';

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
        {() => {
          return (
            <ShopInfo shop={ shop }/>
          )
        }}
      </StateHandler>
    )
  }
}

export default inject('store')(observer(Shop))
