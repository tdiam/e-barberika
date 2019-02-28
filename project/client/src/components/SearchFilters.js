import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { inject, observer } from 'mobx-react'
import { getCurrentDate } from '../utils/getCurrentDate'

class SearchFilters extends Component {

  state = {
    dateFrom: getCurrentDate(),
    dateTo: ''
  }


  submitHandler = (e) => {
    e.preventDefault()
    this.props.setFilters(this.state)
  }

  changeHandler = (e) => {
    this.setState(
      {[e.target.name]: e.target.value
    })
  }

  render () {
    const today = getCurrentDate()
    let filters =
      <>
        <form onSubmit={ this.submitHandler }>
          <label htmlFor="dateFrom">Από</label>
          <input
            type="date"
            name="dateFrom"
            defaultValue={ today }
            /* do not allow dates after today's date or the selected dateTo, if it's earlier */
            max={ (this.state.dateTo !== '') ? ((this.state.dateTo > today) ? today : this.state.dateTo) : today }
            onChange={ this.changeHandler }>
          </input>
          <br></br>
          <label htmlFor="dateTo">Μέχρι</label> 
          <input 
            type="date"
            name="dateTo"
            /* do not allow dates prior to dateFrom */
            min={ this.state.dateFrom }
            onChange={ this.changeHandler }>    
          </input>
        </form>
      </>
    let comp = (this.props.display) ? (filters) : (undefined)
    return (
      <div>
        { comp }
      </div>
    )
  }
}

SearchFilters.propTypes = {
  display: PropTypes.bool.isRequired,
  setFilters: PropTypes.func.isRequired,
}

export default inject('store')(observer(SearchFilters))
