import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { inject, observer } from 'mobx-react'
import MaterialTable from 'material-table'
import { Alert } from 'reactstrap'

import StateHandler from '../components/StateHandler'
import { tagsToText } from '../utils/tags'
import tableOptions from '../utils/tableOptions'


class PriceAdd extends Component {
  constructor(props) {
    super(props)
    this.root = this.props.store
    this.store = this.props.store.shopStore

    this.columns = [{
      title: 'Όνομα καταστήματος',
      field: 'name',
      render: ({ id, name }) => (
        <Link to={ `/shops/${id}` }>{ name }</Link>
      ),
    }, {
      title: 'Διεύθυνση',
      field: 'address',
    }, {
      title: 'Αποσυρμένο',
      field: 'withdrawn',
      type: 'boolean'
    }, {
      title: 'Ετικέτες',
      field: 'tags',
      render: ({ tags }) => tagsToText(tags),
    }]

  }

  async loadShops() {
    // Execute API call that will update the store state
    // NOTE: not too good if we have too many shops
    await this.store.getShops({ count: 0 })
    await this.store.getShops({ count: this.store.pagination.total, status: 'ALL' })
  }

  componentDidMount() {
    if (!this.root.isLoggedIn) {
      this.props.history.push('/')
    }
    this.loadShops()
  }

  render() {
    const { state, shops } = this.store

    return (
      <StateHandler state={ state }>
        <Alert color="info" className="mx-auto mb-4">Επιλέξτε κατάστημα για να καταχωρήσετε τιμή</Alert>
        <MaterialTable
          data={ shops }
          columns={ this.columns }
          title="Λίστα καταστημάτων"
          { ...tableOptions }
          options={{
            actionsColumnIndex: -1,
            pageSize: 10,
            pageSizeOptions: [10, 20, 50]
          }}
        />
      </StateHandler>
    )
  }
}

export default inject('store')(observer(PriceAdd))
