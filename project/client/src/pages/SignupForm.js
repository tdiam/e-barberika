import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

/**
 * Login page.
 *
 * Form-based component, see AddShop.js for an explanation on how we build and use them.
 */
class SignupForm extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store.authStore
  }

  state = { username: '', password: '', email: '' }

  handleChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    })
  }

  handleSubmit = (e) => {
    e.preventDefault()
    this.store.authenticate(this.state.username, this.state.password, this.state.email)
  }

  render () {
    return (
      <form onSubmit={ this.handleSubmit }>
        <div>
          <label htmlFor="username">Username:</label>
          <input name="username" id="username" type="text" required
            value={ this.state.username } onChange={ this.handleChange }></input>
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input name="password" id="password" type="password" required
            value={ this.state.password } onChange={ this.handleChange }></input>
        </div>
        <div>
          <label htmlFor="email">E-mail:</label>
          <input name="email" id="email" type="email" required
            value={ this.state.email } onChange={ this.handleChange }></input>
        </div>
        <button>Sign up</button>
      </form>
    )
  }
}

export default inject('store')(observer(SignupForm))
