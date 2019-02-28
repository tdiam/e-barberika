import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { inject, observer } from 'mobx-react'
import { getCurrentDate } from '../utils/getCurrentDate'

const constDateFrom = getCurrentDate(),
 constDateTo = '',
 constSort = '',
 constSortAttr = 'none',
 constSortType = 'none',
 constGeoDist = -1,
 constGeoLat = -1,
 constGeoLng = -1


class SearchFilters extends Component {

  state = {
    dateFrom: constDateFrom,
    dateTo: constDateTo,
    sort: constSort,
    sort1_attr: constSortAttr,
    sort1_type: constSortType,
    geoDist: constGeoDist,
    geoLat: constGeoLat,
    geoLng: constGeoLng,
  }

  err_msg = ''

  submitHandler = async (e) => {
    e.preventDefault()

    const { 
      dateFrom, dateTo, geoDist, geoLng, geoLat, sort1_type, sort1_attr 
    } = this.state

    // assumes simult set of geo{Lat,Lng}
    const geoFilter = geoDist !== constGeoDist && geoLat !== constGeoLat,
    dateNeedsSync = dateTo === '',
    sortFilter = sort1_type !== 'none' && sort1_attr !== 'none',
    halfSortFilter = (sort1_type !== 'none' && sort1_attr === 'none') || (sort1_type === 'none' && sort1_attr !== 'none')

    if (dateNeedsSync) this.setState({dateTo: dateFrom})
    if (geoDist !== -1 && geoLat === -1) 
      this.err_msg += "Πρέπει να συνδιάσετε το φίλτρο απόστασης με επιλογή σημείου στο χάρτη.\n"
    if (geoDist === -1 && geoLat !== -1) 
      this.err_msg += "Πρέπει να συνδιάσετε την επιλογή σημείου στο χάρτη με το φίλτρο απόστασης.\n"
    if (sortFilter) 
      if (sort1_attr === 'geoDist' && !geoFilter) 
        this.err_msg += "Πρέπει να συμπληρώσετε τα φίλτρα απόστασης για να ταξινομήσετε κατά απόσταση.\n"
      else
        await this.setState({
          sort: `${sort1_attr}|${sort1_type}`
        })
      
    else if (halfSortFilter)
      this.err_msg += "Πρέπει να επιλέξετε και τα δύο ή κανένα πεδίο ταξινόμησης.\n"

    console.log(this.state)

    if (this.err_msg === '') {
      this.props.setFilters({
        dateFrom,
        dateTo,
        geoDist,
        geoLat,
        geoLng,
        sort: this.state.sort
      })
      await this.setState({
        dateFrom: constDateFrom,
        dateTo: constDateTo,
        sort: constSort,
        sort1_attr: constSortAttr,
        sort1_type: constSortType,
        geoDist: constGeoDist,
        geoLat: constGeoLat,
        geoLng: constGeoLng,
      })
    } else {
      window.alert(this.err_msg)
      this.err_msg = '' 
    }
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
      this.state[`sort${i-1}_attr`] !== "none" && 
      this.state[`sort${i-1}_type`] !== "none" &&
      this.state[`sort${i-1}_attr`] &&
      this.state[`sort${i-1}_type`]
      )
    )
  }

  constructSortFilters = () => {
    return (
      /* simplified filter (neoaggelos suggestion) */
        [1].map(i => (
          <React.Fragment key={i}>
            <label htmlFor={ `sort${i}` }>{ "Ταξινόμηση" }</label>
                <select
                  disabled={ !this.sortFieldEnabled(i) } 
                  name={ `sort${i}_attr` }
                  onChange={ this.changeHandler }
                  value={ this.state.sort1_attr }>
                  <option value="none"> -- </option>
                  <option value="geoDist"> Απόσταση </option>
                  <option value="price"> Τιμή </option>
                  <option value="date"> Ημερομηνία </option>
                </select>
                <select 
                  disabled={ !this.sortFieldEnabled(i) }
                  name={ `sort${i}_type` }
                  onChange={ this.changeHandler }
                  value={ this.state.sort1_type }
                >
                  <option value="none"> -- </option>
                  <option value="ASC">Αύξουσα</option>
                  <option value="DESC">Φθίνουσα</option>
                </select>
                <br></br>
          </React.Fragment>
        ))
      )
  }

  constructDateFilters = () => {
    const today = getCurrentDate()
    return (
      <>  
        <label htmlFor="dateFrom">Από</label>
        <input
          type="date"
          name="dateFrom"
          value={ this.state.dateFrom }
          /* do not allow dates after today's date or the selected dateTo, if it's earlier */
          max={ (this.state.dateTo !== '') ? ((this.state.dateTo > today) ? today : this.state.dateTo) : today }
          onChange={ this.changeHandler }>
        </input>
        <br></br>
        <label htmlFor="dateTo">Μέχρι</label> 
        <input
          type="date"
          name="dateTo"
          value={ this.state.dateTo }
          /* do not allow dates prior to dateFrom */
          min={ this.state.dateFrom }
          onChange={ this.changeHandler }>    
        </input>
      </>
    )
  }

  constructMapFilters = () => {
    return (
      <>
        <p>Map goes here</p>
        <label htmlFor="geoDist">Απόσταση</label> 
        <input type="number" name="geoDist"></input>
      </>
    )
  }

  render () {
    let sortFilters = this.constructSortFilters()
    let dateFilters = this.constructDateFilters()
    let mapFilters = this.constructMapFilters()
    let filters = (
      <>
        <form onSubmit={ this.submitHandler }>
          { dateFilters }
          <br></br>
          { sortFilters }
          { /* sortFilters ends in <br> */ }
          { mapFilters }
          <button type="submit">Υποβολή</button>
        </form>
      </>
    )
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
