import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import StateHandler from './StateHandler'
import PropTypes from 'prop-types'
import MaterialTable from 'material-table'

class SearchResults extends Component {
  constructor (props) {
    super(props)
    this.root = this.props.store
    this.store = this.props.store.priceStore

    this.state = {
      modalOpen : false
    }

    this.columns = [{
        title: 'Όνομα προϊόντος',
        field: 'productName',
    }, {
        title: 'Όνομα καταστήματος',
        field: 'shopName',
    }, {
        title: 'Τιμή',
        field: 'price',
    }, {
      title: 'Ημερομηνία',
      field: 'date',
    }]
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

  applyPaginationLogic = (urlps) => {
    urlps.append("count", this.store.pagination.total)
  }

  componentDidMount () {
    console.log(this.props.query)
    let params = new URLSearchParams()
    this.applyQueryLogic(params, this.props.query)
    this.store.getPrices(params)
  }

  componentWillReceiveProps (nextProps) {
    // Execute API call that will update the store state
    console.log(nextProps.query)
    let params = new URLSearchParams()
    this.applyQueryLogic(params, nextProps.query) // by reference
    this.applyFilterLogic(params, nextProps.filters) 
    this.applyPaginationLogic(params)
    this.store.getPrices(params)
  }

  render () {
    let priceItems = (
      <>
        <MaterialTable 
            data={this.store.prices}
            columns={this.columns}
            title={"Products"}
            actions={this.actions}
            options={{
                actionsColumnIndex: -1,
                pageSize: 10,
                pageSizeOptions: [5, 10, 50]
            }}
        />
      </>
    )
    
    // NOTE: enters twice
    return (
      <StateHandler state={ this.store.state }>
        {() => (
          (priceItems.length !== 0) ? (
            <div>
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
