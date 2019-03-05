import React, { Component } from 'react'
import { Provider, inject, observer } from 'mobx-react'
import { Link } from 'react-router-dom'
import MaterialTable from 'material-table'
import { Container, Row, Col, Button, Modal, ModalHeader, ModalBody } from 'reactstrap'

import StateHandler from '../components/StateHandler'
import ProductAddShopPriceModal from '../components/ProductAddShopPriceModal'
import PriceStore from '../stores/PriceStore'

import { tagsToText } from '../utils/tags'
import tableOptions from '../utils/tableOptions'


class Product extends Component {
  constructor (props) {
    super(props)
    this.root = this.props.store
    this.store = this.props.store.productStore
    this.priceStore = this.props.store.priceStore
    // 2nd instance for independency from this.priceStore
    this.modalPriceStore = new PriceStore(this.root)

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
    await this.modalPriceStore.addPrice({
      productId: this.store.product.id,
      ...data,
    })
    if (this.modalPriceStore.state === 'done') {
      this.toggleModal()
      await this.loadShopsForProduct()
    }
  }

  render () {
    const { product } = this.store
    const { prices } = this.priceStore
    const { modalOpen } = this.state
    return (
      <>
        <StateHandler state={ this.store.state }>
          {() => (
            <div>
              <h2 className="mb-4">Προϊόν</h2>
              <Container fluid className="product-info">
                <Row>
                  <Col md={ 7 } className="product-details">
                    <h2 className="product-name">{ product.name }</h2>
                    <p>Κατηγορία: { product.category }</p>
                    <p className="tags">Ετικέτες: { tagsToText(product.tags) }</p>
                  </Col>
                  <Col md={ 5 }>
                    <h4>Περιγραφή</h4>
                    <p className="description">{ product.description }</p>
                  </Col>
                </Row>
              </Container>
              {
                this.root.isLoggedIn && (
                  <Button className="my-5" onClick={ this.toggleModal }>Καταχώρηση τιμής</Button>
                )
              }
              <Modal size="lg" isOpen={ modalOpen } toggle={ this.toggleModal }>
                <ModalHeader toggle={ this.toggleModal }>
                  Καταχώρηση τιμής στο προϊόν { product.name }
                </ModalHeader>
                <ModalBody>
                  <Provider modalPriceStore={ this.modalPriceStore }>
                    <ProductAddShopPriceModal
                      onSubmit={ this.handleSubmit }
                      onCancel={ this.toggleModal }
                    />
                  </Provider>
                </ModalBody>
              </Modal>
            </div>
          )}
        </StateHandler>
        <StateHandler state={ this.priceStore.state }>
          {() => (
            <div>
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
            </div>
          )}
        </StateHandler>
      </>
    )
  }
}

export default inject('store')(observer(Product))
