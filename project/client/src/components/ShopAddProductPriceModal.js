import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

import PriceStore from '../stores/PriceStore'

/**
 * Modal window for editing/creating shops
 * Based on AddShop.original.js
 * <ShopModal parent={parent_component} mode="edit" />
 */
class ShopAddProductPriceModal extends Component {
  constructor(props) {
    super(props)
    this.parent = this.props.parent
    this.root = this.props.store

    // using RootStore.PriceStore would break parent's table
    this.store = new PriceStore(this.root)

    this.state = {
      shopId: this.props.shopId,
      price: null,
      productId: null,
      dateFrom: null,
      dateTo: null
    }
  }

  /**
   * One-size-fits-all change handler for form fields.
   * Changes to a field with name `<field>` will be applied to `state.<field>`.
   * (e.g. `address` -> `state.address`).
   */
  handleChange = (e) => {
    console.log('Changed: ', e.target.name, e.target.value)

    this.setState({
      [e.target.name]: e.target.value,
    })
  }

  handleSubmit = async (e) => {
    // Prevent actual submission of the form
    e.preventDefault()
    // Clear errors
    console.log("Clicked submit, state is ", this.state)

    // Submit request
    // TODO: show notification on error/success
    await this.store.addPrice(this.state)

    // will reload shops
    this.parent.closeModal()
  }

  handleCancel = async (e) => {
    e.preventDefault()
    console.log("Clicked cancel")
    this.parent.closeModal()
  }
  
  async componentDidMount() {
    // get all shops for dropdown selection
    await this.root.productStore.getProducts({'count': 0})
    await this.root.productStore.getProducts({'count': this.root.productStore.pagination.total})

    this.setState({
      productId: this.root.productStore.products[0].id
    })
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <h3>Προσθήκη προϊόντος στο κατάστημα</h3>
        <div>
          <label htmlFor="name">Προϊόν:</label>
          <select name="name" id="name" type="text" required
            value={this.state.productId} onChange={this.handleChange}>
            {
              this.root.productStore.products.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))
            }</select>
        </div>
        <div>
          <label htmlFor="price">Τιμή (σε ευρώ):</label>
          <input name="price" id="price" type="number" required
            value={this.state.price} onChange={this.handleChange}></input>
        </div>
        <div>
          <label htmlFor="dateFrom">Ημερομηνία από:</label>
          <input name="dateFrom" id="dateFrom" type="text" required
            value={this.state.lat} onChange={this.handleChange}></input>
        </div>
        <div>
          <label htmlFor="dateTo">Ημερομηνία έως:</label>
          <input name="dateTo" id="dateTo" type="text" required
            value={this.state.lat} onChange={this.handleChange}></input>
        </div>
        <div style={{float: 'left'}}>
          <button style={{marginRight: '20px'}}>Εισαγωγή</button>
          <button onClick={this.handleCancel}>Ακύρωση</button>
        </div>
      </form>
    )
  }
}

export default inject('store')(observer(ShopAddProductPriceModal))
