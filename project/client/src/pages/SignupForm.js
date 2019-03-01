import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Form, FormGroup, Input, Label, Button, Alert } from 'reactstrap'

import StateHandler from '../components/StateHandler'

/**
 * Signup page.
 */
class SignupForm extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store.authStore
  }

  state = { username: '', password: '' }

  componentDidMount() {
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

  handleSubmit = (e) => {
    e.preventDefault()
    this.store.register(this.state.username, this.state.password)
  }

  render () {
    return (
      <>
        <Form className="signup-form" onSubmit={ this.handleSubmit }>
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
          <Button className="mt-3">Εγγραφή</Button>
          <StateHandler state={ this.store.state } ifPending="">
            <Alert color="secondary">Ο λογαριασμός δημιουργήθηκε και μπορείτε πλέον να συνδεθείτε.</Alert>
          </StateHandler>
        </Form>
      </>
    )
  }
}

export default inject('store')(observer(SignupForm))
