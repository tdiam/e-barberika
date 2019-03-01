/**
 * NOTE: UNUSED, kept only as reference.
 * Delete if deemed appropriate
 */

import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

/**
 * Example of form component that creates a Shop with the entered data.
 *
 * The distinction between internal state and application state is showcased here:
 * - Internal state is for forms, since any change in the fields is not relevant to
 * other parts of the application.
 * - Application state (MobX stores) is only used here for application-level actions,
 * such as addShop (which may then trigger changes to the application state).
 */
class AddShop extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store.shopStore
  }

  state = {
    name: '',
    address: '',
    lng: 0,
    lat: 0,
    error: '',
  }

  /**
   * One-size-fits-all change handler for form fields.
   * Changes to a field with name `<field>` will be applied to `state.<field>`.
   * (e.g. `address` -> `state.address`).
   */
  handleChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    })
  }

  handleSubmit = async (e) => {
    // Prevent actual submission of the form
    e.preventDefault()
    // Clear errors
    this.setState({ error: '' })

    // Submit request
    await this.store.addShop({
      name: this.state.name,
      address: this.state.address,
      lng: this.state.lng,
      lat: this.state.lat,
    })

    // Handle errors
    if (this.store.state === 'error') {
      this.setState({ error: 'The request failed' })
    }
    if (this.store.state === 'unauthorized') {
      this.setState({ error: 'You are not authorized' })
    }
  }

  render () {
    return (
      <form onSubmit={ this.handleSubmit }>
        <h3>Add Shop</h3>
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
          this.state.error && (
            <div style={{ color: 'red' }}>
              { this.state.error }
            </div>
          )}
        <button>Add</button>
      </form>
    )
  }
}

export default inject('store')(observer(AddShop))
