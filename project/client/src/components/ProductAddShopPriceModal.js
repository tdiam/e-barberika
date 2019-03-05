import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Form, FormGroup, Input, Label, Button } from 'reactstrap'

import DateFilter from './search/DateFilter'
import StateHandler from './StateHandler'


/**
 * Modal window for adding a product's price to a shop
 */
class ProductAddShopPriceModal extends Component {
  constructor(props) {
    super(props)
    this.store = this.props.store.shopStore
    this.priceStore = this.props.modalPriceStore
    // dreadful hack
    this.priceStore.setState('done')

    this.state = {
      shopId: '',
      price: '',
      dateFrom: '',
      dateTo: '',
    }
  }
  
  async componentDidMount() {
    // get all products for dropdown selection
    await this.store.getShops({ count: 0 })
    await this.store.getShops({ count: this.store.pagination.total })
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

  preparedHandler = (data) => this.setState(data)

  handleSubmit = async (e) => {
    e.preventDefault()
    const { shopId, price, dateFrom, dateTo } = this.state
    await this.props.onSubmit({ shopId, price, dateFrom, dateTo })
    this.forceUpdate()
  }

  handleCancel = (e) => {
    e.preventDefault()
    this.props.onCancel()
  }

  render() {
    const { shopId, price } = this.state
    return (
      <StateHandler state={ this.priceStore.state }>
        <Form onSubmit={ this.handleSubmit }>
          <FormGroup>
            <Label htmlFor="shopId">Κατάστημα:</Label>
            <Input type="select" name="shopId" id="shopId" required
              value={ shopId } onChange={ this.handleChange }>
              <option value="" disabled hidden>Επιλογή καταστήματος</option>
              { this.store.shops.map(({ id, name }) => (
                <option key={ id } value={ id }>{ name }</option>
              ))}
            </Input>
          </FormGroup>
          <FormGroup>
            <Label htmlFor="price">Τιμή (σε ευρώ):</Label>
            <Input name="price" id="price" type="number" min="0.01" step="0.01" required
              value={ price } onChange={ this.handleChange } />
          </FormGroup>
          <DateFilter onPrepared={ this.preparedHandler } />
          <FormGroup>
            <Button>Εισαγωγή</Button>
            <Button color="dark" onClick={ this.handleCancel }>Ακύρωση</Button>
          </FormGroup>
        </Form>
      </StateHandler>
    )
  }
}

export default inject('store', 'modalPriceStore')(observer(ProductAddShopPriceModal))
