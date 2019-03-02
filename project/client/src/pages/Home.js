import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Form, Alert } from 'reactstrap'

import SearchBar from '../components/SearchBar'
import SearchResults from '../components/SearchResults'
import SearchFilters from '../components/SearchFilters'

class Home extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store.priceStore
  }

  state = {
    query: '',
    filters: {},
    error: '',
    showFilters: false,
    showError: '',
    showResults: false,
  }

  applyQueryLogic = (urlps, query) => {
    const tags = query.split(' ')
    tags.forEach(tag => (urlps.append('tags', tag)))
  }

  applyFilterLogic = (urlps, filters) => {
    for (const attr in filters) {
      urlps.append(attr, filters[attr])
    }
  }

  fetchPrices () {
    let params = new URLSearchParams()
    this.applyQueryLogic(params, this.state.query)
    this.applyFilterLogic(params, this.state.filters)
    console.debug(params.toString())
    this.store.getPrices(params)
  }

  submitHandler = (e) => {
    e.preventDefault()
    // Hide everything at first and then decide which ones to show
    // showError is a string and maintains error message between submissions
    this.setState({ showError: '', showFilters: false, showResults: false })

    // If there isn't a query, show nothing
    if (this.state.query === '') return

    // Else
    // Show filters when query exists
    this.setState({ showFilters: true })
    // If there is a form error, show it and keep results hidden
    if (this.state.error !== '') {
      this.setState({ showError: this.state.error })
    } else {
      // Otherwise fetch prices and show results
      this.fetchPrices()
      this.setState({ showResults: true })
    }
  }

  preparedHandler = (data) => this.setState(data)

  render () {
    const { showFilters, showError, showResults } = this.state
    return (
      <>
        <Form className="hero-search" onSubmit={ this.submitHandler }>
          <h2>Αναζήτηση τιμών</h2>
          <SearchBar onPrepared={ this.preparedHandler } />
          { showFilters && (
            <SearchFilters
              onPrepared={ this.preparedHandler }
            />
          )}
          { showError !== '' && (
            <Alert error="danger">{ showError }</Alert>
          )}
        </Form>
        { showResults && (
          <SearchResults />
        )}
      </>
    )
  }
}

export default inject('store')(observer(Home))
