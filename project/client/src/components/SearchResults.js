import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import MaterialTable from 'material-table'
import { Link } from 'react-router-dom'

import StateHandler from './StateHandler'
import tableOptions from '../utils/tableOptions'

class SearchResults extends Component {
  constructor (props) {
    super(props)
    this.root = this.props.store
    this.store = this.props.store.priceStore

    this.state = {
      modalOpen: false,
    }

    this.columns = [{
      title: 'Όνομα προϊόντος',
      field: 'productName',
      render: rowData => {
        return (
          <Link to={`/products/${rowData.productId}`}>{rowData.productName}</Link>
        )
      },
    }, {
      title: 'Όνομα καταστήματος',
      field: 'shopName',
      render: rowData => {
        return (
          <Link to={`/shops/${rowData.shopId}`}>{rowData.shopName}</Link>
        )
      },
    }, {
      title: 'Τιμή',
      field: 'price',
    }, {
      title: 'Ημερομηνία',
      field: 'date',
    }, {
      title: 'Απόσταση (km)',
      field: 'shopDist',
      render: rowData => {
        return Math.round(rowData.shopDist)
      },
    }]
  }

  render () {
    const prices = this.store.prices

    // NOTE: enters twice
    return (
      <StateHandler state={ this.store.state }>
        {() => (prices.length > 0) ? (
          <div className="search-results">
            <MaterialTable
              data={ prices }
              columns={ this.columns }
              title="Αποτελέσματα"
              actions={ this.actions }
              {...tableOptions}
              options={{
                actionsColumnIndex: -1,
                pageSize: 10,
                pageSizeOptions: [5, 10, 20, 50],
              }} />
          </div>
        ) : (
          <div className="search-results">
            <h2>Δε βρέθηκαν προϊόντα!</h2>
          </div>
        )}
      </StateHandler>
    )
  }
}

export default inject('store')(observer(SearchResults))
