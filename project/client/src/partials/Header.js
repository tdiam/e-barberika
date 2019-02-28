import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { inject, observer } from 'mobx-react'

/**
 * Common header component.
 */
class Header extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store
  }

  handleLogout = () => this.store.clearUser()

  render () {
    let userAction
    if (this.store.isLoggedIn) {
      // Show log out button if user is logged in
      userAction = (<button onClick={ this.handleLogout }>Log out</button>)
    } else {
      // Otherwise show log in button
      userAction = (<><Link to="/login">Log in</Link> | <Link to="/signup">Sign up</Link> </>)
    }

    const hello = (
      <>
        <h3>
          { this.store.userOrGuest }!
        </h3>
        <h3>
          { userAction }
        </h3>
      </>
    )

    return (
      <nav>
        <h1><Link to="/">ΠΑΡΑΤΗΡΗΤΗΡΙΟ</Link></h1>
        { hello }
        <ul>
          <li><Link to="/shops">Shops</Link></li>
          { /* Example of hiding restricted pages */
            this.store.isLoggedIn && <li><Link to="/shops/add">Add Shop</Link></li>
          }
          <li><Link to="/map">Map</Link></li>
        </ul>
      </nav>
    )
  }
}

export default inject('store')(observer(Header))
