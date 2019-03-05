import React, { Component } from 'react'
import { Provider, inject, observer } from 'mobx-react'
import { Link } from 'react-router-dom'
import MaterialTable from 'material-table'
import { Container, Row, Col, Button, Modal, ModalHeader, ModalBody } from 'reactstrap'

import StateHandler from '../components/StateHandler'
import ShopAddProductPriceModal from '../components/ShopAddProductPriceModal'
import Map from '../components/Map'
import Marker from '../components/MapMarker'
import PriceStore from '../stores/PriceStore'

import { tagsToText } from '../utils/tags'
import tableOptions from '../utils/tableOptions'


class Shop extends Component {
  constructor (props) {
    super(props)
    this.root = this.props.store
    this.store = this.props.store.shopStore
    this.priceStore = this.props.store.priceStore
    // 2nd instance for independency from this.priceStore
    this.modalPriceStore = new PriceStore(this.root)

    this.columns = [{
      'title': 'Προϊόν',
      'field': 'productName',
      'render': ({ productId, productName }) => (
        <Link to={ `/products/${productId}` }>{ productName }</Link>
      ),
    }, {
      'title': 'Ετικέτες Προϊόντος',
      'field': 'productTags',
      'render': ({ productTags }) => tagsToText(productTags),
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
    // Fetch shop with given ID
    await this.store.getShop(this.props.match.params.id)
    await this.loadProductsForShop()
  }

  async loadProductsForShop() {
    if (this.store.state === 'done') {
      const ids = [this.store.shop.id]
      await this.priceStore.getPrices({ shops: ids, count: 0 })
      await this.priceStore.getPrices({ shops: ids, count: this.priceStore.pagination.total })
    }
  }

  toggleModal = () => this.setState(prevState => ({
    modalOpen: !prevState.modalOpen,
  }))

  handleSubmit = async (data) => {
    await this.modalPriceStore.addPrice({
      shopId: this.store.shop.id,
      ...data,
    })
    if (this.modalPriceStore.state === 'done') {
      this.toggleModal()
      await this.loadProductsForShop()
    }
  }

  render () {
    const { shop, state } = this.store
    const coords = [shop.lat, shop.lng]
    const { prices } = this.priceStore
    const { modalOpen } = this.state
    return (
      <>
        <StateHandler state={ state }>
          {() => (
            <div>
              <Container fluid className="shop-info">
                <Row>
                  <Col md={ 5 } className="shop-details">
                    <h2 className="shop-name">{ shop.name }</h2>
                    <p>{ shop.address }</p>
                    <p className="tags">Ετικέτες: { tagsToText(shop.tags) }</p>
                  </Col>
                  <Col md={ 7 } className="shop-map">
                    <Map center={ coords }
                      zoom={ 11 }
                      height={ 400 }>
                      <Marker anchor={ coords } text={ shop.name } />
                    </Map>
                  </Col>
                </Row>
              </Container>
              <Modal size="lg" isOpen={ modalOpen } toggle={ this.toggleModal }>
                <ModalHeader toggle={ this.toggleModal }>
                  Καταχώρηση τιμής στο κατάστημα { shop.name }
                </ModalHeader>
                <ModalBody>
                  <Provider modalPriceStore={ this.modalPriceStore }>
                    <ShopAddProductPriceModal
                      onSubmit={ this.handleSubmit }
                      onCancel={ this.toggleModal }
                    />
                  </Provider>
                </ModalBody>
              </Modal>
            </div>
          )}
        </StateHandler>
        <StateHandler state={ state }>
          {() => (
            <div>
              {
                this.root.isLoggedIn && (
                  <Button className="my-5" onClick={ this.toggleModal }>Καταχώρηση τιμής</Button>
                )
              }
              <MaterialTable
                { ...tableOptions }
                data={ prices }
                columns={ this.columns }
                title='Διαθέσιμα Προϊόντα'
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

export default inject('store')(observer(Shop))
