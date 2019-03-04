import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Button } from 'reactstrap'

import { DateFilter, GeoFilter } from './search/filters'

class SearchFilters extends Component {
  state = {
    dateFrom: '',
    dateTo: '',
    geoDist: '',
    geoLat: '',
    geoLng: '',
    dateError: '',
    geoError: '',
  }

  error () {
    const { dateError, geoError } = this.state
    // Get non-empty errors and join them with new lines
    return [dateError, geoError].filter(x => x !== '').join('\n')
  }

  prepareData () {
    const { dateFrom, dateTo, geoDist, geoLat, geoLng } = this.state

    // Check if there is any error
    let error = this.error(),
        filters = {}

    if (error === '') {
      // if no errors, set filters to send to parent
      filters = { dateFrom, dateTo }
      // add geo filter if it's set
      if (geoDist !== '') {
        filters = { ...filters, geoDist, geoLat, geoLng }
      }
    }

    this.props.onPrepared({ filters, error })
  }

  componentDidUpdate (_prevProps, prevState) {
    if (this.state !== prevState) {
      this.prepareData()
    }
  }

  preparedHandler = (data) => this.setState(data)

  render() {
    return (
      <>
        <DateFilter
          onPrepared={ this.preparedHandler } />
        <GeoFilter
          onPrepared={ this.preparedHandler } />
        <Button>Αναζήτηση</Button>
      </>
    )
  }
}

SearchFilters.propTypes = {
  onPrepared: PropTypes.func.isRequired,
}
 
export default SearchFilters