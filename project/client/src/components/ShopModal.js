import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Form, FormGroup, Input, Button, Label } from 'reactstrap'

import TagInput from './TagInput'
import Map from './Map'
import Draggable from './MapDraggable'


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
    // Region level view when editing, country view when creating
    const zoomLevel = this.props.mode === 'edit' ? 11 : 4
    return (
      <Form onSubmit={ this.handleSubmit }>
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
        <Map center={[38.008928, 23.747025]} zoom={ zoomLevel } width={ 600 } height={ 400 }>
          <Draggable
            anchor={[lat, lng]}
            offset={[16, 32]}
            onDragEnd={ ([lat, lng]) => this.setState({ lat, lng }) }
          >
            <img src="img/pin.svg" alt="Επιλογή τοποθεσίας" width="32" height="32" />
          </Draggable>
        </Map>
        <FormGroup>
          <Label htmlFor="tags">Ετικέτες:</Label>
          <TagInput tag={ Input } name="tags" id="tags"
            value={ tags } onChange={ this.handleTagsChange }></TagInput>
        </FormGroup>
        <FormGroup>
          <Button>Αποθήκευση</Button>
          <Button color="dark" onClick={ this.handleCancel }>Ακύρωση</Button>
        </FormGroup>
      </Form>
    )
  }
}

export default inject('store')(observer(ShopModal))
