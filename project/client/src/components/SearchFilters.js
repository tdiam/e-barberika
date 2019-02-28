import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { inject, observer } from 'mobx-react'
import { getCurrentDate } from '../utils/getCurrentDate'

class SearchFilters extends Component {

  state = {
    dateFrom: getCurrentDate(),
    dateTo: '',
    sort: '',
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

  sortFieldEnabled = (i) => {
    return (
      i===1 || (
      this.sortFieldEnabled(i-1) &&
      this.state[`sort${i-1}-attr`] !== "none" && 
      this.state[`sort${i-1}-type`] !== "none" &&
      this.state[`sort${i-1}-attr`] &&
      this.state[`sort${i-1}-type`]
      )
    )
  }

  render () {
    const today = getCurrentDate()
    let sortFilters =  
      [1,2,3].map(i => (
        <React.Fragment key={i}>
          <label htmlFor={ `sort${i}` }>{ `${i}ο Κριτήριο Ταξινόμησης` }</label>
              <select
                disabled={ !this.sortFieldEnabled(i) } 
                name={ `sort${i}-attr` }
                onChange={ this.changeHandler }
                defaultValue="none">
                <option value="none"> -- </option>
                <option value="geoDist"> Απόσταση </option>
                <option value="price"> Τιμή </option>
                <option value="date"> Ημερομηνία </option>
              </select>
              <select 
                disabled={ !this.sortFieldEnabled(i) }
                name={ `sort${i}-type` }
                onChange={ this.changeHandler }
                defaultValue="none"  
              >
                <option value="none"> -- </option>
                <option name="asc">Αύξουσα</option>
                <option name="desc">Φθίνουσα</option>
              </select>
              <br></br>
        </React.Fragment>
      ))
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
          <br></br>
          { sortFilters }

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
