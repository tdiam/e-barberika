import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

import ProductInfo from '../components/ProductInfo'
import StateHandler from '../components/StateHandler'

class Product extends Component {
  constructor (props) {
    super(props)
    this.store = props.store.productStore
  }
  componentDidMount () {
    // Fetch shop with given ID
    this.store.getProduct(this.props.match.params.id)
  }
  render () {
    const { product, state } = this.store
    return (
      <StateHandler state={state}>
        {() => {
          return (
            <ProductInfo product={ product }/>
          )
        }}
      </StateHandler>
    )
  }
}

export default inject('store')(observer(Product))
