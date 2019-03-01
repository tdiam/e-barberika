import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { inject, observer } from 'mobx-react'

class ProductInfo extends Component {

  render () {
    let product = this.props.product
    const tagList = product.tags.map(tag => (
        <li key={ tag }>{ tag }</li>
    ))
    return (
      <div>
        <h2>Προϊόν</h2>
        <dl>
        <dt><h3>{ product.name }</h3></dt>
        <dd><h5> Κατηγορία: { product.category }</h5></dd>
        </dl>
        <p style={{borderStyle: 'inset'}}>Περιγραφή: { product.description }</p>
        <p> Ετικέτες </p>
        <ul className='taglist'>
        { tagList }
        </ul>
        <p>{ (product.withdrawn) ? 'Αποσυρμένο' : ''}</p>
      </div>
    )
  }
}

ProductInfo.propTypes = {
  product: PropTypes.object.isRequired,
}

export default inject('store')(observer(ProductInfo))
