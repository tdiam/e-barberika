import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { inject, observer } from 'mobx-react'
import { Button, Input, Form, FormGroup, Label, Row, Col } from 'reactstrap'

import { getCurrentDate } from '../utils/getCurrentDate'

const constDateFrom = getCurrentDate(),
 defaultDateTo = '',
 defaultSort = undefined,
 defaultSortAttr = 'none',
 defaultSortType = 'none',
 defaultGeoDist = '',
 defaultGeoLat = '',
 defaultGeoLng = ''


class SearchFilters extends Component {


  /**
   * @var {String} sort1_attr: name of html sort attribute (values: 'geoDist' / 'date' / 'price'),
   *  1 in name is legacy from multiple sorting filters
   */
  state = {
    dateFrom: constDateFrom,
    dateTo: defaultDateTo,
    sort: defaultSort,
    sort1_attr: defaultSortAttr,
    sort1_type: defaultSortType,
    geoDist: defaultGeoDist,
    geoLat: defaultGeoLat,
    geoLng: defaultGeoLng,
  }

  err_msg = ''

  /**
   * Handle filter-form submission
   * 
   * @param {Event} e
   * @returns Nothing
   */
  submitHandler = async (e) => {
    e.preventDefault()

    let { 
      dateFrom, dateTo, geoDist, geoLng, geoLat, sort1_type, sort1_attr 
    } = this.state

    // assumes simultaneous set of geo{Lat,Lng}
    const geoFilter = geoDist !== defaultGeoDist && geoLat !== defaultGeoLat,
    dateToNeedsSync = dateTo === defaultDateTo,
    dateFromNeedsSync = dateFrom === defaultDateTo,
    sortFilter = sort1_type !== defaultSortType && sort1_attr !== defaultSortAttr,
    halfSortFilter = 
      (sort1_type !== defaultSortType && sort1_attr === defaultSortAttr) 
      || 
      (sort1_type === defaultSortType && sort1_attr !== defaultSortAttr)

    /* specs: both or neither dates */
    console.log(dateToNeedsSync, dateFromNeedsSync)
    if (dateToNeedsSync && dateFromNeedsSync)
      await this.setState({dateFrom: undefined})
    else if (dateToNeedsSync) await this.setState({dateTo: dateFrom})
    else if (dateFromNeedsSync) await this.setState({dateFrom: dateTo}) 
    
    /* specs: all three all none of them */
    console.log(geoDist)
    if (geoDist !== defaultGeoDist && geoLat === defaultGeoLat)
      this.err_msg += "Πρέπει να συνδιάσετε το φίλτρο απόστασης με επιλογή σημείου στο χάρτη.\n"
    if (geoDist === defaultGeoDist && geoLat !== defaultGeoLat) 
      this.err_msg += "Πρέπει να συνδιάσετε την επιλογή σημείου στο χάρτη με το φίλτρο απόστασης.\n"
    
    /* if sorting was "properly" selected */
    if (sortFilter) 
      /* check if user sorts by distance without setting geoFilter */
      if (sort1_attr === 'geoDist' && !geoFilter) 
        this.err_msg += "Πρέπει να συμπληρώσετε τα φίλτρα απόστασης για να ταξινομήσετε κατά απόσταση.\n"
      else
        await this.setState({
          sort: `${sort1_attr}|${sort1_type}`
        })
    
    /* if only one of the 2 fields was selected */
    else if (halfSortFilter)
      this.err_msg += "Πρέπει να επιλέξετε και τα δύο ή κανένα πεδίο ταξινόμησης.\n"
    /* else sort is `Empty` as far as `SearchResults` is concerned */

    /* if no error occured, use setFilters to notify Home */
    if (this.err_msg === '') {
      
      if (geoFilter)
        this.props.setFilters({
          dateFrom: this.state.dateFrom,
          dateTo: this.state.dateTo,
          geoDist,
          geoLat,
          geoLng,
          sort: this.state.sort
        })
      else 
        this.props.setFilters({
          dateFrom: this.state.dateFrom,
          dateTo: this.state.dateTo,
          sort: this.state.sort
        })

      /* reset (for semantics) */
      this.setState({
        dateFrom: constDateFrom,
        dateTo: defaultDateTo,
        sort: defaultSort,
        sort1_attr: defaultSortAttr,
        sort1_type: defaultSortType,
        geoDist: defaultGeoDist,
        geoLat: defaultGeoLat,
        geoLng: defaultGeoLng,
      })

    } else { /* if a semantic error occured, notify and leave state as is */
      window.alert(this.err_msg)
      this.err_msg = '' // otherwise it will accumulate 
    }
  }

  changeHandler = (e) => {
    this.setState(
      {[e.target.name]: e.target.value
    })
  }

  /**
   * If multiple sort filters can be used, restrict change on sorting filters
   * with lower prio from the highest prio unset filter
   * 
   * @param {integer} i
   * @returns `true` if all filters with prio  <`i` have been `properly` (no semantics) set  
   */
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
    const numOfSortingFilters = 1 
    let possibleSortingFilters = Array.apply(null, Array(numOfSortingFilters))
    possibleSortingFilters = possibleSortingFilters.map((x, i) => (i+1))
    return (
      /* simplified filter (neoaggelos suggestion) */
      possibleSortingFilters.map(i => (
        <FormGroup key={i}>
          <Label htmlFor={ `sort${i}` }>{ "Ταξινόμηση" }</Label>
          <Row form>
            <Col md={ 6 }>
              <Input type="select"
                disabled={ !this.sortFieldEnabled(i) } 
                name={ `sort${i}_attr` }
                onChange={ this.changeHandler }
                value={ this.state.sort1_attr }>
                <option value="none"> -- </option>
                <option value="geoDist"> Απόσταση </option>
                <option value="price"> Τιμή </option>
                <option value="date"> Ημερομηνία </option>
              </Input>
            </Col>
            <Col md={ 6 }>
              <Input type="select" 
                disabled={ !this.sortFieldEnabled(i) }
                name={ `sort${i}_type` }
                onChange={ this.changeHandler }
                value={ this.state.sort1_type }
              >
                <option value="none"> -- </option>
                <option value="ASC">Αύξουσα</option>
                <option value="DESC">Φθίνουσα</option>
              </Input>
            </Col>
          </Row>
        </FormGroup>
      ))
    )
  }

  constructDateFilters = () => {
    const today = getCurrentDate()
    return (
      <Row form>
        <Col md={ 6 }>
          <FormGroup>
            <Label htmlFor="dateFrom">Από</Label>
            <Input
              type="date"
              name="dateFrom"
              value={ this.state.dateFrom }
              /* do not allow dates after today's date or the selected dateTo, if it's earlier */
              max={ (this.state.dateTo !== '') ? ((this.state.dateTo > today) ? today : this.state.dateTo) : today }
              onChange={ this.changeHandler }>
            </Input>
          </FormGroup>
        </Col>
        <Col md={ 6 }>
          <FormGroup>
            <Label htmlFor="dateTo">Μέχρι</Label> 
            <Input
              type="date"
              name="dateTo"
              value={ this.state.dateTo }
              /* do not allow dates prior to dateFrom */
              min={ this.state.dateFrom }
              onChange={ this.changeHandler }>    
            </Input>
          </FormGroup>
        </Col>
      </Row>
    )
  }

  constructMapFilters = () => {
    return (
      <FormGroup>
        <p>Map goes here</p>
        <Label htmlFor="geoDist">Απόσταση</Label> 
        <Input 
          type="number" step="1" min="1" 
          name="geoDist"
          onChange={ this.changeHandler }
        >
        </Input>
      </FormGroup>
    )
  }

  render () {
    /* let sortFilters = this.constructSortFilters() */
    let dateFilters = this.constructDateFilters()
    let mapFilters = this.constructMapFilters()
    let filters = (
      <>
        <Form onSubmit={ this.submitHandler }>
          { dateFilters }
          {/* sortFilters */}
          { mapFilters }
          <Button>Υποβολή</Button>
        </Form>
      </>
    )
    return (
      <div className="search-filters">
        { filters }
      </div>
    )
  }
}

SearchFilters.propTypes = {
  setFilters: PropTypes.func.isRequired,
}
 

export default inject('store')(observer(SearchFilters))
