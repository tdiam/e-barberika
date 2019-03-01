import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

/**
 * Modal window for editing/creating shops
 * Based on AddShop.original.js
 * <ShopModal parent={parent_component} mode="edit" />
 */
class ShopModal extends Component {
  constructor (props) {
    super(props)
    this.parent = this.props.parent
    this.store = this.props.parent.store.shop
    this.mode = this.props.mode

    if (this.mode === 'edit') {
      console.log(this.store)
      this.state = {
        id: this.id,
        name: this.store.name,
        address: this.store.address,
        lng: this.store.lng,
        lat: this.store.lat,
        tags: this.store.tags,
        withdrawn: this.store.withdrawn
      }
    }
  }

  state = {
    name: '',
    address: '',
    lng: 0,
    lat: 0,
    tags: [],
    error: false,
    message: ''
  }

  /**
   * One-size-fits-all change handler for form fields.
   * Changes to a field with name `<field>` will be applied to `state.<field>`.
   * (e.g. `address` -> `state.address`).
   */
  handleChange = (e) => {
    console.log('Changed: ', e.target.name, e.target.value)
    if (e.target.name === 'tags') {
      console.log('ignoring tags')
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
    this.setState({ error: true, message: 'clicked send' })

    console.log("Clicked submit, mode is ", this.mode)

    // Submit request
    // await this.store.addShop({
    //   name: this.state.name,
    //   address: this.state.address,
    //   lng: this.state.lng,
    //   lat: this.state.lat,
    // })

    // Handle errors
    // if (this.store.state === 'error') {
      // this.setState({ error: 'The request failed' })
    // }
    // if (this.store.state === 'unauthorized') {
      // this.setState({ error: 'You are not authorized' })
    // }
  }

  handleCancel = async (e) => {
    e.preventDefault()
    this.setState({ error: '' })
    console.log("Clicked cancel")
    this.parent.closeModal()

  }

  render () {
    return (
      <form onSubmit={ this.handleSubmit }>
        <h3>{this.mode === 'edit' ? 'Επεξεργασία' : 'Δημιουργία'} Καταστήματος</h3>
        <div>
          <label htmlFor="name">Name:</label>
          <input name="name" id="name" type="text" required
            value={ this.state.name } onChange={ this.handleChange }></input>
        </div>
        <div>
          <label htmlFor="address">Address:</label>
          <input name="address" id="address" type="text" required
            value={ this.state.address } onChange={ this.handleChange }></input>
        </div>
        <div>
          <label htmlFor="lat">Latitude:</label>
          <input name="lat" id="lat" type="number" step="any" min="-90" max="90" required
            value={ this.state.lat } onChange={ this.handleChange }></input>
        </div>
        <div>
          <label htmlFor="lng">Longitude:</label>
          <input name="lng" id="lng" type="number" step="any" min="-90" max="90" required
            value={ this.state.lng } onChange={ this.handleChange }></input>
        </div>
        { // Errors
          this.state.message && (
            <div style={{ color: 'red' }}>
              { this.state.message }
            </div>
          )}
        <button>{this.mode}</button>
        <button onClick={this.handleCancel}>Cancel</button>
      </form>
    )
  }
}

export default inject('store')(observer(ShopModal))
