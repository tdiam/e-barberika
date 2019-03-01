import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import SearchBar from '../components/SearchBar'
// import SearchField from 'react-search-field';
import SearchResults from '../components/SearchResults'
import SearchFilters from '../components/SearchFilters'

class Home extends Component {
  state = {
    query: '',
    filters: {},
  }

  setQuery = (query) => {
    this.setState({ query })
  }

  setFilters = (filters) => {
    this.setState({ filters })
  }

  showFilters = () => {
    return this.state.query !== ''
  }

  render () {
    return (
      <>
        <div className="hero-search">
          <h2>Αναζήτηση τιμών</h2>
          <SearchBar setQuery={ this.setQuery } />
          <SearchFilters
            display={ this.showFilters() }
            setFilters={ this.setFilters }
          />
        </div>
        <SearchResults
          query={ this.state.query }
          filters={ this.state.filters }
        />
      </>
    )
  }
}

export default inject('store')(observer(Home))
