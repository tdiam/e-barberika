import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

/**
 * Login page.
 * 
 * Form-based component, see AddShop.js for an explanation on how we build and use them.
 */
class LoginForm extends Component {
    constructor(props) {
        super(props)
        this.store = this.props.store.authStore
    }

    state = { username: '', password: '', message: '' }

    handleChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        })
    }

    handleSubmit = async (e) => {
        e.preventDefault()
        await this.store.authenticate(this.state.username, this.state.password)
        /*
         redirect
         src: https://gist.github.com/elitan/5e4cab413dc201e0598ee05287ee4338
         */
        if (this.store.rootStore.user.username) this.props.history.push('/')
        else this.setState({password: '', message: 'Incorrect username or password!'})
    }

    render() {
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
                <p style={{color: '#ff0000'}}>{ this.state.message }</p>
                <button>Log in</button>
            </form>
        )
    }
}

export default inject('store')(observer(LoginForm))