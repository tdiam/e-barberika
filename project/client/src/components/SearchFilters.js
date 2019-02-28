import React, { Component } from 'react'
import PropTypes from 'prop-types';
import { inject, observer } from 'mobx-react'
import { getCurrentDate } from '../utils/getCurrentDate';
import { action, decorate, observable } from 'mobx'


class SearchFilters extends Component {

  filters = observable({
    dateFrom: getCurrentDate(),
    dateTo: ''
  })

  submitHandler = (e) => {
    e.preventDefault()
    this.props.setFilters(this.filters)
  }

  changeHandler = (e) => {
    this.filters[e.target.name] = e.target.value
  }
  
  render() {
    const today = getCurrentDate()
    let filters = 
      <React.Fragment>
        <form onSubmit={ this.submitHandler }>
          <label htmlFor="dateFrom">Από</label> 
          <input 
            type="date"
            name="dateFrom"
            defaultValue={ today }
            /* do not allow dates after today's date or the selected dateTo, if it's earlier */
            max={ (this.filters.dateTo !== '') ? ((this.filters.dateTo > today) ? today : this.filters.dateTo) : today }
            onChange={ this.changeHandler }>
          </input>
          <br></br>
          <label htmlFor="dateTo">Μέχρι</label> 
          <input 
            type="date"
            name="dateTo"
            /* do not allow dates prior to dateFrom */
            min={ this.filters.dateFrom }
            onChange={ this.changeHandler }>    
          </input>
        </form>
      </React.Fragment>
    let comp = (this.props.display) ? (filters) : (undefined)
    return(
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

decorate(SearchFilters, {
  changeHandler: action,
})

export default inject('store')(observer(SearchFilters))