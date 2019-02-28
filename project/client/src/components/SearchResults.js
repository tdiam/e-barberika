import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import StateHandler from './StateHandler';
import PropTypes from 'prop-types';


class SearchResults extends Component {
  constructor(props) {
    super(props)
    this.store = this.props.store
  }

  state = {
    pending: <p></p>
  }

  componentWillReceiveProps(nextProps) {
    // Execute API call that will update the store state
    let params = new URLSearchParams();
    let tags = nextProps.query.split(" ")
    tags.forEach(tag => (params.append("tags", tag)))
    this.store.priceStore.getPrices(params)
  }
  
  render() {
    let priceItems = this.store.priceStore.prices.map(price => (
      <li key={ `${price.shopId}:${price.productId}` }>{ price.productName }, { price.shopName }, { price.price }</li>))
    return (
      <StateHandler state={ this.store.priceStore.state } ifPending={ this.state.pending }>
      {() => (
            (priceItems.length !== 0) ? (
              <div>
                <h2>Product, Shop, Price:</h2>
                  <ul>
                    { priceItems }
                  </ul>
              </div>
             ) : 
             (<h2>Δε βρέθηκαν προϊόντα!</h2>)
      )}
      </StateHandler>
    )
  }
}

SearchResults.propTypes = {
  query: PropTypes.string.isRequired,
  filters: PropTypes.object.isRequired,
}

export default inject('store')(observer(SearchResults))