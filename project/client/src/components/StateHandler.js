import React, { Component } from 'react'

const defaultPending = (
    <>Φόρτωση...</>
)

const defaultError = (
    <div className="error">Κάτι πήγε στραβά!</div>
)

const defaultUnauthorized = defaultError

const componentOrFunction = (cf) => {
    // If is React element return it as is
    if(React.isValidElement(cf)) {
        return cf
    }
    // Otherwise try to call the function
    return cf()
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
    render() {
        if(this.props.state === 'done') return componentOrFunction(this.props.children)
        if(this.props.state === 'pending') return componentOrFunction(this.props.ifPending)
        if(this.props.state === 'error') return componentOrFunction(this.props.ifError)
        if(this.props.state === 'unauthorized') return componentOrFunction(this.props.ifUnauthorized)
    }
}
StateHandler.defaultProps = {
    ifPending: defaultPending,
    ifError: defaultError,
    ifUnauthorized: defaultUnauthorized,
}

export default StateHandler