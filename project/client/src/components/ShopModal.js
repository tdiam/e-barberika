import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Form, FormGroup, Input, Button, Label } from 'reactstrap'

import TagInput from './TagInput'


/**
 * Modal window for editing/creating shops
 */
class ShopModal extends Component {
  constructor(props) {
    super(props)
    this.store = this.props.store.shopStore

    if (this.props.mode === 'edit') {
      const { id, name, address, lng, lat, tags, withdrawn } = this.store.shop
      this.state = { id, name, address, lng, lat, tags, withdrawn }
    } else {
      this.state = {
        id: null,
        name: '',
        address: '',
        lng: '',
        lat: '',
        tags: [],
        withdrawn: false,
      }
    }
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

  handleTagsChange = (tags) => this.setState({ tags })

  handleSubmit = (e) => {
    // Prevent actual submission of the form
    e.preventDefault()

    const { id, name, address, lng, lat, tags } = this.state
    // id is null if mode === 'create'
    // parent component should ignore it
    this.props.onSubmit(id, { name, address, lng, lat, tags })
  }

  handleCancel = (e) => {
    e.preventDefault()
    this.props.onCancel()
  }

  render() {
    const { name, address, lat, lng, tags } = this.state
    return (
      <Form onSubmit={ this.handleSubmit }>
        <h3>{ this.props.mode === 'edit' ? 'Επεξεργασία Στοιχείων' : 'Δημιουργία' } Καταστήματος</h3>
        <FormGroup>
          <Label htmlFor="name">Όνομα:</Label>
          <Input name="name" id="name" type="text" required
            value={ name } onChange={ this.handleChange }></Input>
        </FormGroup>
        <FormGroup>
          <Label htmlFor="address">Διεύθυνση:</Label>
          <Input name="address" id="address" type="text" required
            value={ address } onChange={ this.handleChange }></Input>
        </FormGroup>
        <FormGroup>
          <Label htmlFor="lat">Latitude:</Label>
          <Input name="lat" id="lat" type="number" step="any" min="-90" max="90" required
            value={ lat } onChange={ this.handleChange }></Input>
        </FormGroup>
        <FormGroup>
          <Label htmlFor="lng">Longitude:</Label>
          <Input name="lng" id="lng" type="number" step="any" min="-180" max="180" required
            value={ lng } onChange={ this.handleChange }></Input>
        </FormGroup>
        <FormGroup>
          <Label htmlFor="tags">Ετικέτες:</Label>
          <TagInput tag={ Input } name="tags" id="tags"
            value={ tags } onChange={ this.handleTagsChange }></TagInput>
        </FormGroup>
        <FormGroup>
          <Button>Αποθήκευση</Button>
          <Button onClick={ this.handleCancel }>Ακύρωση</Button>
        </FormGroup>
      </Form>
    )
  }
}

export default inject('store')(observer(ShopModal))
