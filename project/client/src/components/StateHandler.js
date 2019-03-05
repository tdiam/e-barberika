import React, { Component } from 'react'
import { Alert } from 'reactstrap'

const defaultPending = (
  <div>Φόρτωση...</div>
)

const defaultError = (
  <Alert color="danger">Κάτι πήγε στραβά!</Alert>
)

const defaultUnauthorized = (
  <Alert color="danger">
    Δεν έχετε δικαιώματα να εκτελέσετε αυτήν την ενέργεια.
    Παρακαλούμε ελέγξτε μήπως έληξε η συνεδρία σας.
  </Alert>
)

const getComponent = (cf) => {
  // If is pure string, turn it into a component
  if (typeof cf === 'string') {
    return (<>{ cf }</>)
  }
  // If it is a function, call it and return results
  if (typeof cf === 'function') {
    return cf()
  }
  // If nully, return null
  if (cf == null) {
    return null
  }
  // Otherwise return as is
  return cf
}

/**
 * Given a store's state and a component, this function decides whether
 * to render the component, or display an error message or a pending
 * message.
 *
 * To avoid undefined errors you can also pass components as functions
 * that return them. See docs for more details.
 *
 * @param {String} state Store state. One of "pending", "done",
 * "unauthorized", "error".
 * @param {React.Component} children A function that returns the component
 * to be rendered if state is equal to "done".
 * @param {React.Component} [ifPending] The component to be
 * rendered if state is equal to "pending".
 * @param {React.Component} [ifError] The component to be
 * rendered if state is equal to "error".
 * @param {React.Component} [ifUnauthorized] The component to be
 * rendered if state is equal to "unauthorized".
 * @returns {React.Component} Resulting component.
 */
class StateHandler extends Component {
  render () {
    if (this.props.state === 'done') return getComponent(this.props.children)
    if (this.props.state === 'pending') return getComponent(this.props.ifPending)
    if (this.props.state === 'error') return getComponent(this.props.ifError)
    if (this.props.state === 'unauthorized') return getComponent(this.props.ifUnauthorized)
    throw new Error(`Unexpected state value: ${this.props.state}`)
  }
}
StateHandler.defaultProps = {
  ifPending: defaultPending,
  ifError: defaultError,
  ifUnauthorized: defaultUnauthorized,
}

export default StateHandler
