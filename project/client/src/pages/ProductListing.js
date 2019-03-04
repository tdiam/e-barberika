import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { inject, observer } from 'mobx-react'
import MaterialTable from 'material-table'
import { Button, Modal, ModalHeader, ModalBody } from 'reactstrap'

import ProductModal from '../components/ProductModal'
import StateHandler from '../components/StateHandler'
import { tagsToText } from '../utils/tags'
import tableOptions from '../utils/tableOptions'


class ProductListing extends Component {
  constructor(props) {
    super(props)
    this.root = this.props.store
    this.store = this.props.store.productStore

    this.state = {
      modalMode: null
    }

    this.columns = [{
      title: 'Όνομα Προϊόντος',
      field: 'name',
      render: ({ id, name }) => (
        <Link to={ `/products/${id}` }>{ name }</Link>
      ),
    }, {
      title: 'Κατηγορία',
      field: 'category',
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
          this.store.getProduct(id)
          this.openModal('edit')
        },
        icon: 'edit',
        name: 'Επεξεργασία προϊόντος'
      }, {
        onClick: async (e, { id }) => {
          await this.store.deleteProduct(id)
          this.loadProducts()
        },
        icon: 'delete',
        name: 'Διαγραφή προϊόντος'
      }]
    } else {
      this.actions = []
    }

  }

  async loadProducts() {
    // Execute API call that will update the store state
    // NOTE: not too good if we have too many products
    await this.store.getProducts({ count: 0 })
    await this.store.getProducts({ count: this.store.pagination.total, status: 'ALL' })
  }

  componentDidMount() {
    this.loadProducts()
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
        this.store.addProduct(data)
        this.closeModal()
        this.loadProducts()
      }
    } else if (mode === 'edit') {
      return (id, data) => {
        this.store.editProduct(id, data)
        this.closeModal()
        this.loadProducts()
      }
    }
  }

  render() {
    const { state, products } = this.store
    const { modalMode } = this.state

    return (
      <StateHandler state={ state }>
        { this.root.isLoggedIn && (
          <Button onClick={ () => this.openModal('create') }>Εισαγωγή προϊόντος</Button>
        )}
        <MaterialTable
          data={ products }
          columns={ this.columns }
          title="Λίστα προϊόντων"
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
            { modalMode === 'edit' ? 'Επεξεργασία στοιχείων' : 'Δημιουργία' } προϊόντος
          </ModalHeader>
          <ModalBody>
            <ProductModal
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

export default inject('store')(observer(ProductListing))
