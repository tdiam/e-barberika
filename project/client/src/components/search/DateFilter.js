import React, { Component } from 'react'
import { Input, FormGroup, Label, Row, Col } from 'reactstrap'

import { getCurrentDate } from '../../utils/getCurrentDate'

class DateFilter extends Component {
  constructor (props) {
    super(props)
    this.today = getCurrentDate()
    this.state = {
      dateFrom: this.today,
      dateTo: '',
    }
    this.prepareData()
  }
  changeHandler = (e) => {
    this.setState({
      [e.target.name]: e.target.value
    })
  }
  /**
   * Prepare data for parent.
   * If dateFrom and dateTo are both empty, clear filter.
   * If one of them is empty, make it equal to the other.
   */
  prepareData () {
    let { dateFrom, dateTo } = this.state
    // dateError is currently empty for all cases
    let dateError = ''
    if (!dateFrom && !dateTo) {
      dateFrom = dateTo = undefined
    } else if (!dateFrom) {
      dateFrom = dateTo
    } else if (!dateTo) {
      dateTo = dateFrom
    }
    this.props.onPrepared({ dateFrom, dateTo, dateError })
  }
  /**
   * Fires every time the state changes.
   * Checks if values have changed as advised in docs:
   * https://reactjs.org/docs/react-component.html#componentdidupdate
   */
  componentDidUpdate (_prevProps, prevState) {
    if (this.state.dateFrom !== prevState.dateFrom || this.state.dateTo !== prevState.dateTo) {
      this.prepareData()
    }
  }
  render() {
    let maxDateFrom
    /**
     * If dateTo is set and is before today, then this is the max value for dateFrom.
     * Otherwise, it is today.
     */
    if (this.state.dateTo !== '' || this.state.dateTo < this.today) {
      maxDateFrom = this.state.dateTo
    } else {
      maxDateFrom = this.today
    }
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
              max={ maxDateFrom }
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
}
 
export default DateFilter