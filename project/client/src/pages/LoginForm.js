import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Form, FormGroup, Label, Input, Button, Alert } from 'reactstrap'

import StateHandler from '../components/StateHandler'

/**
 * Login page.
 *
 * Form-based component, see AddShop.js for an explanation on how we build and use them.
 */
class LoginForm extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store.authStore
  }

  state = { username: '', password: '' }

  componentDidMount() {
    if (this.store.rootStore.isLoggedIn) {
      this.props.history.push('/')
    }
    this.store.resetState()
  }

  componentWillUnmount() {
    this.store.resetState()
  }

  handleChange = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    })
  }

  handleSubmit = async (e) => {
    e.preventDefault()
    await this.store.authenticate(this.state.username, this.state.password)
    if (this.store.rootStore.isLoggedIn) {
      this.props.history.push('/')
    } else {
      this.setState({ username: '', password: '' })
    }
  }

  render () {
    if (this.store.rootStore.isLoggedIn) {
      return null
    }

    const UnauthorizedAlert = (
      <Alert color="danger">Το όνομα χρήστη ή ο κωδικός πρόσβασης είναι λανθασμένα!</Alert>
    )

    return (
      <Form className="login-form" onSubmit={ this.handleSubmit }>
        <FormGroup>
          <Label htmlFor="username">Όνομα χρήστη:</Label>
          <Input name="username" id="username" type="text" required
            value={ this.state.username } onChange={ this.handleChange }></Input>
        </FormGroup>
        <FormGroup>
          <Label htmlFor="password">Κωδικός πρόσβασης:</Label>
          <Input name="password" id="password" type="password" required
            value={ this.state.password } onChange={ this.handleChange }></Input>
        </FormGroup>
        <Button className="mt-3">Σύνδεση</Button>
        <StateHandler state={ this.store.state } ifUnauthorized={ UnauthorizedAlert } ifPending=""></StateHandler>
      </Form>
    )
  }
}

export default inject('store')(observer(LoginForm))
