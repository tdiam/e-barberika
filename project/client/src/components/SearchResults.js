import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import StateHandler from './StateHandler';


class SearchResults extends Component {
  constructor(props) {
    super(props)
    this.store = this.props.store
  }
  //Needs to be updated automatically with action?
  runQuery = () =>{
    // Execute API call that will update the store state
    let params = new URLSearchParams();
    let tags = this.props.query.split(" ")
    tags.forEach(tag => (params.append("tags", tag)))
    //console.log(params.keys())
    this.store.priceStore.getPrices(params)
  }

  shopName = (id) => {
    this.store.shopStore.getShop(id)
    return this.store.shopStore.shop.name
  }

  productName = (id) => {
    this.store.productStore.getShop(id)
    return this.store.productStore.product.name
  }
  
  render() {
    let priceItems = this.store.priceStore.prices.map(price => (
      <li>{ this.productName(price.productId) }, { this.shopName(price.shopId) }, { price.price }</li>))
    return (
      <StateHandler state={ this.store.priceStore.state }>
      {() => (
        <div>
          <h2>Product, Shop, Price:</h2>
            <ul>
              { priceItems }
            </ul>
        </div>
      )}
      </StateHandler>
    )
  }
}


export default inject('store')(observer(SearchResults))