import React, { Component } from 'react'

class SingleProduct extends Component {
  

  
  render () {
    return (
        <div>
            <ProductInfo id={ /* id from url */ }/>
        </div>
    )
  }
}

export default inject('store')(observer(SingleProduct))
