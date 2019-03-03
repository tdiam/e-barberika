import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { inject, observer } from 'mobx-react'
import { Link } from 'react-router-dom'

import MaterialTable from 'material-table'
import Popup from 'reactjs-popup'

import Map from '../components/Map'
import Marker from '../components/MapMarker'
import Overlay from '../components/MapOverlay'

import ShopAddProductPriceModal from '../components/ShopAddProductPriceModal'

import { tagsToText } from '../utils/tags'

class ShopInfo extends Component {
  constructor(props) {
    super(props)
    this.root = this.props.store
    this.priceStore = this.root.priceStore
    this.shop = this.props.shop
    this.tags_text = tagsToText(this.shop.tags)

    this.columns = [{
      'title': 'Προϊόν',
      'field': 'productName',
      'render': rowData => (<Link to={"/products/" + rowData.productId + "/"}>{rowData.productName}</Link>)
    }, {
      'title': 'Ετικέτες Προϊόντος',
      'field': 'productTags',
      'render': rowData => (tagsToText(rowData.productTags))
    }, {
      'title': 'Τιμή',
      'field': 'price',
      'type': 'currency'
    }]

    this.state = {
      modalOpen: false
    }
  }

  async componentDidMount() {
    this.loadProductsForShop()
  }

  async loadProductsForShop() {
    if (this.shop.id !== undefined) {
      await this.priceStore.getPrices({ shops: this.shop.id, count: 0 })
      await this.priceStore.getPrices({ shops: this.shop.id, count: this.priceStore.pagination.total })
    }
  }

  openModal() {
    this.setState({
      modalOpen: true
    })
  }

  closeModal() {
    this.setState({
      modalOpen: false
    })
    this.loadProductsForShop()
  }

  render() {
    const shop = this.shop
    const coords = [shop.lat, shop.lng]
    return (
      <div>
        <div>
          <h2>Κατάστημα</h2>
          <h3> Όνομα Καταστήματος: {shop.name}</h3>
          <p> Διεύθυνση: {shop.address}</p>
          <p> Ετικέτες: {tagsToText(shop.tags)} </p>
          <Map center={coords}
            zoom={11}
            width={600} height={400}>
            <Marker anchor={coords} />
            <Overlay anchor={coords}>{shop.name}</Overlay>
          </Map>
        </div>
        {this.root.isLoggedIn && (<button onClick={(e) => this.openModal()}>Καταχώρηση Τιμής</button>)}
        <MaterialTable
          data={this.priceStore.prices}
          columns={this.columns}
          title={'Διαθέσιμα Προϊόντα'}
          options={{
            pageSize: 10,
            pageSizeOptions: [10, 20, 50]
          }}
        />
        <Popup
          open={this.state.modalOpen}
          closeOnDocumentClick={false}
          closeOnEscape={false}
        >
          <ShopAddProductPriceModal parent={this} shopId={shop.id} />
        </Popup>

      </div>
    )
  }
}

ShopInfo.propTypes = {
  shop: PropTypes.object.isRequired
}

export default inject('store')(observer(ShopInfo))
