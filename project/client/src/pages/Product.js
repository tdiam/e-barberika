import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Link } from 'react-router-dom'
import MaterialTable from 'material-table'
import { Button, Modal, ModalHeader, ModalBody } from 'reactstrap'

import StateHandler from '../components/StateHandler'
import ProductAddShopPriceModal from '../components/ProductAddShopPriceModal'

import { tagsToText } from '../utils/tags'
import tableOptions from '../utils/tableOptions'


class Product extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store.productStore
    this.priceStore = this.props.store.priceStore

    this.columns = [{
      'title': 'Κατάστημα',
      'field': 'shopName',
      'render': ({ shopId, shopName }) => (
        <Link to={ `/shops/${shopId}` }>{ shopName }</Link>
      ),
    }, {
      'title': 'Ετικέτες Καταστήματος',
      'field': 'shopTags',
      'render': ({ shopTags }) => tagsToText(shopTags),
    }, {
      'title': 'Τιμή',
      'field': 'price',
      'type': 'currency',
      'render': ({ price }) => `${price.toFixed(2)}€`,
    }]

    this.state = {
      modalOpen: false,
    }
  }

  async componentDidMount () {
    // Fetch product with given ID
    await this.store.getProduct(this.props.match.params.id)
    await this.loadShopsForProduct()
  }

  async loadShopsForProduct() {
    if (this.store.state === 'done') {
      const ids = [this.store.product.id]
      await this.priceStore.getPrices({ products: ids, count: 0 })
      await this.priceStore.getPrices({ products: ids, count: this.priceStore.pagination.total })
    }
  }

  toggleModal = () => this.setState(prevState => ({
    modalOpen: !prevState.modalOpen,
  }))

  handleSubmit = async (data) => {
    this.toggleModal()
    await this.priceStore.addPrice({
      productId: this.store.product.id,
      ...data,
    })
    await this.loadShopsForProduct()
  }

  render () {
    const { product, state } = this.store
    const { prices } = this.priceStore
    const { modalOpen } = this.state
    return (
      <StateHandler state={ state }>
        {() => (
          <div>
            <div>
              <h2>Προϊόν</h2>
              <h3>Όνομα Προϊόντος: { product.name }</h3>
              <p>Κατηγορία: { product.category }</p>
              <p>Περιγραφή: { product.description }</p>
              <p>Ετικέτες: { tagsToText(product.tags) }</p>
            </div>
            <Button onClick={ this.toggleModal }>Καταχώρηση Τιμής</Button>
            <MaterialTable
              { ...tableOptions }
              data={ prices }
              columns={ this.columns }
              title='Διαθέσιμο στα Καταστήματα'
              options={{
                pageSize: 10,
                pageSizeOptions: [10, 20, 50]
              }}
            />
            <Modal size="lg" isOpen={ modalOpen } toggle={ this.toggleModal }>
              <ModalHeader toggle={ this.toggleModal }>
                Καταχώρηση τιμής στο προϊόν { product.name }
              </ModalHeader>
              <ModalBody>
                <ProductAddShopPriceModal
                  onSubmit={ this.handleSubmit }
                  onCancel={ this.toggleModal }
                />
              </ModalBody>
            </Modal>
          </div>
        )}
      </StateHandler>
    )
  }
}

export default inject('store')(observer(Product))
