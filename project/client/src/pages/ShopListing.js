import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { inject, observer } from 'mobx-react'

import MaterialTable from 'material-table'
import Popup from 'reactjs-popup'
import tableOptions from '../utils/tableOptions';

import ShopModal from '../components/ShopModal'
import { tagsToText } from '../utils/tags'

class ShopListing extends Component {
  constructor(props) {
    super(props)
    this.root = this.props.store
    this.store = this.props.store.shopStore

    this.state = {
      modalOpen: false,
      modalMode: null
    }

    this.columns = [{
      title: 'Όνομα καταστήματος',
      field: 'name',
      render: rowData => (<Link to={"/shops/" + rowData.id}>{rowData.name}</Link>)
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
      render: rowData => (tagsToText(rowData.tags))
    }]

    if (this.root.isLoggedIn) {
      this.actions = [{
        this: this,
        onClick: async function (e, rowData) {
          /* `this`: action object */
          /* `this.this`: ShopListing object */
          this.this.store.getShop(rowData.id)
          this.this.openModal('edit')
        },
        icon: 'edit',
        name: 'Επεξεργασία καταστήματος'
      }, {
        this: this,
        onClick: async function (e, rowData) {
          await this.this.store.deleteShop(rowData.id)
          await this.this.loadShops()
        },
        icon: 'delete',
        name: 'Διαγραφή καταστήματος'
      }]
    } else {
      this.actions = []
    }

  }

  async loadShops() {
    // Execute API call that will update the store state
    // NOTE: not too good if we have too many shops
    await this.store.getShops({ count: 0 })
    await this.store.getShops({ count: this.store.pagination.total, status: 'ALL' })
  }

  async componentDidMount() {
    await this.loadShops()
  }

  openModal(mode = 'edit') {
    this.setState({
      modalOpen: true,
      modalMode: mode
    })
  }

  closeModal() {
    this.setState({
      modalOpen: false,
      modalMode: null
    })
  }

  render() {
    //DEBUG
    // if (! this.root.isLoggedIn) {
    //     return (
    //         <div>
    //             You must log in
    //         </div>
    //     )
    // }
    if (this.store.state === 'done') {
      return (
        <>
          {
            this.root.isLoggedIn && (
              <button onClick={(e) => { this.openModal('create') }}>Εισαγωγή καταστήματος</button>
            )
          }
          <MaterialTable
            data={this.store.shops}
            columns={this.columns}
            title={"Λίστα καταστημάτων"}
            {...tableOptions}
            actions={this.actions}
            options={{
              actionsColumnIndex: -1,
              pageSize: 10,
              pageSizeOptions: [10, 20, 50]
            }}
          />
          <Popup
            closeOnDocumentClick={false}
            closeOnEscape={false}
            open={this.state.modalOpen}
          >

            <ShopModal parent={this} mode={this.state.modalMode} />
          </Popup>
        </>
      )
    }
    return (
      <div>
        <p>pending</p>
      </div>
    )
  }
}

export default inject('store')(observer(ShopListing))
