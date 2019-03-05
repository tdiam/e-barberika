import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { FormGroup, Input, Button } from 'reactstrap'

export default class SearchBar extends Component {
  changeHandler = (e) => {
    this.props.onPrepared({ query: e.target.value })
  }

  render () {
    return (
      <FormGroup className="search-bar">
        <Input
          type="text"
          name="query"
          placeholder="Αναζήτηση με ετικέτες..."
          onChange={ this.changeHandler }
          text={ this.props.query }
        />
        <Button>Αναζήτηση</Button>
      </FormGroup>
    )
  }
}

SearchBar.propTypes = {
  query: PropTypes.string,
  onPrepared: PropTypes.func.isRequired,
}
