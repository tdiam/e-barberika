import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

class SearchResults extends Component {
  runQuery = () => {
    // Execute API call that will update the store state
    let params = new URLSearchParams();
    let tags = this.props.query.split(" ")
    tags.map(tag => (params.append("tags", tag)))
    console.log(params.keys())
    this.props.store.getPrices(params)
  }
  
  render() {
    return (
      <div>
        
      </div>
    )
  }
}


export default inject('store')(observer(SearchResults))