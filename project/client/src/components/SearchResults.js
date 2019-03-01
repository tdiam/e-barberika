import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import StateHandler from './StateHandler'
import PropTypes from 'prop-types'

class SearchResults extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store.priceStore
  }

  applyQueryLogic = (urlps, query) => {
    const tags = query.split(' ')
    tags.forEach(tag => (urlps.append('tags', tag)))
  }

  applyFilterLogic = (urlps, filters) => {
    const { dateFrom, dateTo, geoDist, geoLat, geoLng, sort } = filters
    const geoFilter = (geoDist !== undefined)
    const dateFilter = (dateFrom !== undefined)
    const sortingFilter = (sort !== undefined)
    
    if (dateFilter) {
      urlps.append("dateFrom", dateFrom)
      urlps.append("dateTo", dateTo)
    }
    if (geoFilter) {
      urlps.append("geoDist", geoDist)
      urlps.append("geoLat", geoLat)
      urlps.append("geoLng", geoLng)
    }
    if (sortingFilter)
      urlps.append("sort", sort)
  }

  componentWillReceiveProps (nextProps) {
    // Execute API call that will update the store state
    let params = new URLSearchParams()
    this.applyQueryLogic(params, nextProps.query) // by reference
    this.applyFilterLogic(params, nextProps.filters) 
    this.store.getPrices(params)
  }

  render () {
    let priceItems = this.store.prices.map(price => (
      <li key={ `${price.shopId}:${price.productId}` }>
        { price.productName }, { price.shopName }, { price.price }, { price.date }
      </li>
    ))
    // NOTE: enters twice
    return (
      <StateHandler state={ this.store.state }>
        {() => (
          (priceItems.length !== 0) ? (
            <div>
              <h2>Product, Shop, Price:</h2>
              <ul>
                { priceItems }
              </ul>
            </div>
          ) : (
            <h2>Δε βρέθηκαν προϊόντα!</h2>
          )
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
