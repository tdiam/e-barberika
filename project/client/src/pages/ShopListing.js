import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { inject, observer } from 'mobx-react'
import MaterialTable from 'material-table'
import { Button, Modal, ModalHeader, ModalBody } from 'reactstrap'

import ShopModal from '../components/ShopModal'
import StateHandler from '../components/StateHandler'
import { tagsToText } from '../utils/tags'
import tableOptions from '../utils/tableOptions'


class ShopListing extends Component {
  constructor(props) {
    super(props)
    this.root = this.props.store
    this.store = this.props.store.shopStore

    this.state = {
      modalMode: null
    }

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

    if (this.root.isLoggedIn) {
      this.actions = [{
        onClick: async (e, { id }) => {
          this.store.getShop(id)
          this.openModal('edit')
        },
        icon: 'edit',
        name: 'Επεξεργασία καταστήματος'
      }, {
        onClick: async (e, { id }) => {
          await this.store.deleteShop(id)
          this.loadShops()
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

  componentDidMount() {
    this.loadShops()
  }

  openModal = (mode) => {
    this.setState({
      modalMode: mode
    })
  }

  closeModal = () => {
    this.setState({
      modalMode: null
    })
  }

  /**
   * Returns a submit handler function for the given mode.
   * @param {String} mode One of 'create', 'edit'.
   */
  makeSubmitHandler (mode) {
    if (mode === 'create') {
      return (_id, data) => {
        this.store.addShop(data)
        this.closeModal()
        this.loadShops()
      }
    } else if (mode === 'edit') {
      return (id, data) => {
        this.store.editShop(id, data)
        this.closeModal()
        this.loadShops()
      }
    }
  }

  render() {
    const { state, shops } = this.store
    const { modalMode } = this.state

    return (
      <StateHandler state={ state }>
        { this.root.isLoggedIn && (
          <Button className="mb-4" onClick={ () => this.openModal('create') }>
            Εισαγωγή καταστήματος
          </Button>
        )}
        <MaterialTable
          data={ shops }
          columns={ this.columns }
          title="Λίστα καταστημάτων"
          { ...tableOptions }
          actions={ this.actions }
          options={{
            actionsColumnIndex: -1,
            pageSize: 10,
            pageSizeOptions: [10, 20, 50]
          }}
        />
        <Modal size="lg" isOpen={ modalMode != null } toggle={ this.closeModal }>
          <ModalHeader toggle={ this.closeModal }>
            { modalMode === 'edit' ? 'Επεξεργασία στοιχείων' : 'Δημιουργία' } καταστήματος
          </ModalHeader>
          <ModalBody>
            <ShopModal
              mode={ modalMode }
              onSubmit={ this.makeSubmitHandler(modalMode) }
              onCancel={ this.closeModal }
            />
          </ModalBody>
        </Modal>
      </StateHandler>
    )
  }
}

export default inject('store')(observer(ShopListing))
