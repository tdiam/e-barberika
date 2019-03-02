import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

import { tagsToText, textToTags } from '../utils/tags'

/**
 * Modal window for editing/creating shops
 * Based on AddShop.original.js
 * <ShopModal parent={parent_component} mode="edit" />
 */
class ShopModal extends Component {
  constructor(props) {
    super(props)
    this.parent = this.props.parent
    this.store = this.props.parent.store
    this.mode = this.props.mode

    if (this.mode === 'edit') {
      this.state = {
        id: this.store.shop.id,
        name: this.store.shop.name,
        address: this.store.shop.address,
        lng: this.store.shop.lng,
        lat: this.store.shop.lat,
        tags: this.store.shop.tags,
        tags_text: tagsToText(this.store.shop.tags),
        withdrawn: this.store.shop.withdrawn
      }

      // console.log(this.state)
    }
  }

  state = {
    id: null,
    name: '',
    address: '',
    lng: 0,
    lat: 0,
    tags: [],
    tags_text: "",
    withdrawn: false
  }

  /**
   * One-size-fits-all change handler for form fields.
   * Changes to a field with name `<field>` will be applied to `state.<field>`.
   * (e.g. `address` -> `state.address`).
   */
  handleChange = (e) => {
    console.log('Changed: ', e.target.name, e.target.value)
    if (e.target.name === 'tags') {
      // special handling for tags
      // console.log(e.target.value, typeof(e.target.value), textToTags(e.target.value))
      this.setState({
        tags_text: e.target.value,
        tags: textToTags(e.target.value)
      })
    } else {
      this.setState({
        [e.target.name]: e.target.value,
      })
    }
  }

  handleSubmit = async (e) => {
    // Prevent actual submission of the form
    e.preventDefault()
    // Clear errors
    console.log("Clicked submit, mode is ", this.mode)

    // Submit request
    // TODO: show notification on error/success

    let shop = {
      id: this.state.id,
      name: this.state.name,
      address: this.state.address,
      lat: this.state.lat,
      lng: this.state.lng,
      tags: this.state.tags
    }

    if (this.mode === 'create') {
      console.log('Creating shop', shop)
      await this.store.addShop(shop)
    } else if (this.mode === 'edit') {
      console.log('Editing shop', shop)
      await this.store.editShop(shop.id, shop)
    }

    await this.parent.loadShops()
    this.parent.closeModal()
  }

  handleCancel = async (e) => {
    e.preventDefault()
    this.setState({ error: '' })
    console.log("Clicked cancel")
    this.parent.closeModal()
  }


  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <h3>{this.mode === 'edit' ? 'Επεξεργασία Στοιχείων' : 'Δημιουργία'} Καταστήματος</h3>
        <div>
          <label htmlFor="name">Name:</label>
          <input name="name" id="name" type="text" required
            value={this.state.name} onChange={this.handleChange}></input>
        </div>
        <div>
          <label htmlFor="address">Address:</label>
          <input name="address" id="address" type="text" required
            value={this.state.address} onChange={this.handleChange}></input>
        </div>
        <div>
          <label htmlFor="lat">Latitude:</label>
          <input name="lat" id="lat" type="number" step="any" min="-90" max="90" required
            value={this.state.lat} onChange={this.handleChange}></input>
        </div>
        <div>
          <label htmlFor="lng">Longitude:</label>
          <input name="lng" id="lng" type="number" step="any" min="-180" max="180" required
            value={this.state.lng} onChange={this.handleChange}></input>
        </div>
        <div>
          <label htmlFor="tags">Ετικέτες:</label>
          <input name="tags" id="tags" type="text"
            value={this.state.tags_text} onChange={this.handleChange}></input>
        </div>
        <div style={{float: 'left'}}>
          <button style={{marginRight: '20px'}}>{this.mode}</button>
          <button onClick={this.handleCancel}>Cancel</button>
        </div>
      </form>
    )
  }
}

export default inject('store')(observer(ShopModal))
