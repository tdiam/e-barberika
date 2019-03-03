import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Link } from 'react-router-dom'
import MaterialTable from 'material-table'
import Popup from 'reactjs-popup'
import { Button } from 'reactstrap'

import StateHandler from '../components/StateHandler'
import ShopAddProductPriceModal from '../components/ShopAddProductPriceModal'
import Map from '../components/Map'
import Marker from '../components/MapMarker'
import Overlay from '../components/MapOverlay'

import { tagsToText } from '../utils/tags'
import tableOptions from '../utils/tableOptions'


class Shop extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store.shopStore
    this.priceStore = this.props.store.priceStore

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

  openModal = () => {
    this.setState({
      modalOpen: true
    })
  }

  closeModal = () => {
    this.setState({
      modalOpen: false
    })
  }

  handleSubmit = async (data) => {
    this.closeModal()
    await this.priceStore.addPrice({
      shopId: this.store.shop.id,
      ...data,
    })
    await this.loadProductsForShop()
  }

  render () {
    const { shop, state } = this.store
    const coords = [shop.lat, shop.lng]
    const { prices } = this.priceStore
    const { modalOpen } = this.state
    return (
      <StateHandler state={ state }>
        {() => (
          <div>
            <div>
              <h2>Κατάστημα</h2>
              <h3>Όνομα Καταστήματος: { shop.name }</h3>
              <p>Διεύθυνση: { shop.address }</p>
              <p>Ετικέτες: { tagsToText(shop.tags) }</p>
              <Map center={ coords }
                zoom={ 11 }
                width={ 600 } height={ 400 }>
                <Marker anchor={ coords } />
                <Overlay anchor={ coords }>{ shop.name }</Overlay>
              </Map>
            </div>
            <Button onClick={ this.openModal }>Καταχώρηση Τιμής</Button>
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
            <Popup open={ modalOpen } onClose={ this.closeModal }>
              <ShopAddProductPriceModal
                onSubmit={ this.handleSubmit }
                onCancel={ this.closeModal }
              />
            </Popup>
          </div>
        )}
      </StateHandler>
    )
  }
}

export default inject('store')(observer(Shop))
