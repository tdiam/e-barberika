import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Form, FormGroup, Input, Button, Label } from 'reactstrap'

import TagInput from './TagInput'
import StateHandler from './StateHandler'


/**
 * Modal window for editing/creating products
 */
class ProductModal extends Component {
  constructor(props) {
    super(props)
    this.store = this.props.modalProductStore
    // dreadful hack
    this.store.setState('done')

    if (this.props.mode === 'edit') {
      const { id, name, description, category, tags, withdrawn } = this.store.product
      this.state = { id, name, description, category, tags, withdrawn }
    } else {
      this.state = {
        id: null,
        name: '',
        description: '',
        category: '',
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

    const { id, name, description, category, tags } = this.state
    // id is null if mode === 'create'
    // parent component should ignore it
    this.props.onSubmit(id, { name, description, category, tags })
  }

  handleCancel = (e) => {
    e.preventDefault()
    this.props.onCancel()
  }

  render() {
    const { name, description, category, tags } = this.state
    return (
      <StateHandler state={ this.store.state }>
        <Form onSubmit={ this.handleSubmit }>
          <FormGroup>
            <Label htmlFor="name">Όνομα:</Label>
            <Input name="name" id="name" type="text" required
              value={ name } onChange={ this.handleChange }></Input>
          </FormGroup>
          <FormGroup>
            <Label htmlFor="category">Κατηγορία:</Label>
            <Input name="category" id="category" type="text" required
              value={ category } onChange={ this.handleChange }></Input>
          </FormGroup>
          <FormGroup>
            <Label htmlFor="description">Περιγραφή:</Label>
            <Input name="description" id="description" type="textarea" required
              value={ description } onChange={ this.handleChange }></Input>
          </FormGroup>
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
      </StateHandler>
    )
  }
}

export default inject('modalProductStore')(observer(ProductModal))
