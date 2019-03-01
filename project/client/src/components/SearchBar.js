import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Input, Button } from 'reactstrap'

export default class SearchBar extends Component {
  state = {
    searchbar: '',
  }

  handleChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    })
  }

  submitHandler = (e) => {
    e.preventDefault()
    this.props.setQuery(this.state.searchbar)
  }

  render () {
    return (
      <div className="search-bar">
        <form onSubmit={ this.submitHandler }>
          <Input
            type="text"
            name="searchbar"
            placeholder="Αναζήτηση με ετικέτες..."
            onChange={ this.handleChange }
            text={ this.state.searchbar }
          />
          <Button>Go</Button>
        </form>
      </div>
    )
  }
}

SearchBar.propTypes = {
  setQuery: PropTypes.func.isRequired,
}
