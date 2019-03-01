import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { inject, observer } from 'mobx-react'
import { UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap'


class UserActions extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store
  }

  handleLogout = (e) => {
    e.preventDefault()
    this.store.clearUser()
  }

  render() {
    return (
      <UncontrolledDropdown nav inNavbar>
        <DropdownToggle nav caret>
          { this.store.userOrGuest }
        </DropdownToggle>
        { this.store.isLoggedIn ? (
          <DropdownMenu right>
            <DropdownItem onClick={ this.handleLogout }>Αποσύνδεση</DropdownItem>
          </DropdownMenu>
        ) : (
          <DropdownMenu right>
            <DropdownItem tag={ Link } to="/login">Σύνδεση</DropdownItem>
            <DropdownItem tag={ Link } to="/register">Εγγραφή</DropdownItem>
          </DropdownMenu>
        )}
      </UncontrolledDropdown>
    )
  }
}

export default inject('store')(observer(UserActions))