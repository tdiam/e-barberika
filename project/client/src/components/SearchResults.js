import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import StateHandler from './StateHandler';


class SearchResults extends Component {
  constructor(props) {
    super(props)
    this.store = this.props.store
  }
  
  componentWillReceiveProps(nextProps) {
    // Execute API call that will update the store state
    
    let params = new URLSearchParams();
    let tags = nextProps.query.split(" ")
    tags.forEach(tag => (params.append("tags", tag)))
    //console.log(params.keys())
    console.log(this.props.query)
    console.log(nextProps.query)
    this.store.priceStore.getPrices(params)
  }
  
  render() {
    let priceItems = this.store.priceStore.prices.map(price => (
      <li key={ /* "hashing" */ price.productId + price.shopId }>{ price.productName }, { price.shopName }, { price.price }</li>))
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