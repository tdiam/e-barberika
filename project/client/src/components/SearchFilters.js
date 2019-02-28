import React, { Component } from 'react'
import PropTypes from 'prop-types';
import { inject, observer } from 'mobx-react'
import { getCurrentDate } from '../utils/getCurrentDate';
import { action, decorate, observable } from 'mobx'


class SearchFilters extends Component {

  state = observable({
    dateFrom: getCurrentDate(),
    dateTo: '',
  })

  submitHandler = (e) => {
    e.preventDefault()
    this.props.setFilters(this.state.filters)
  }

  changeHandler = (e) => {
    this.setState({
      [e.target.name]: e.target.value
    })
    console.log(this.state.dateFrom)
    console.log(this.state.dateTo)
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
            max={ (this.state.dateTo !== '') ? ((this.state.dateTo > today) ? today : this.state.dateTo) : today }
            onChange={ this.changeHandler }>
          </input>
          <br></br>
          <label htmlFor="dateFrom">Μέχρι</label> 
          <input 
            type="date"
            name="dateΤο"
            min={ this.state.dateFrom }
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