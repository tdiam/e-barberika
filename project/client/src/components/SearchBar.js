import React, { Component } from 'react'
import PropTypes from 'prop-types';

export default class SearchBar extends Component {  
  
  state = {
      searchbar: '',
  }

  handleChange = (e) => {
    this.setState({
        [e.target.name]: e.target.value
    })
  }

  submitHandler = (e) => {
    e.preventDefault()
    this.props.setQuery(this.state.searchbar)
  }

  render() {
    return (
      <div>
        <form onSubmit={ this.submitHandler }>  
            <input 
                type="text" 
                name="searchbar" 
                id="searchbar"
                onChange={ this.handleChange }
                text={ this.state.searchbar }
            />
            <button type="submit">-></button>
        </form>
      </div>
    )
  }
}

SearchBar.propTypes = {
    setQuery: PropTypes.func.isRequired,
}