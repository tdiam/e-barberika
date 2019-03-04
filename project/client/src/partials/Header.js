import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Navbar, NavbarBrand, NavbarToggler, NavItem, NavLink, Collapse, Nav } from 'reactstrap'

import UserActions from '../components/nav/UserActions'

/**
 * Common header component.
 */
class Header extends Component {
  constructor (props) {
    super(props)
    this.store = this.props.store
  }

  state = {
    isOpen: false
  }

  toggle = () => this.setState({ isOpen: !this.state.isOpen })

  render () {
    return (
      <Navbar color="dark" dark expand="lg">
        <NavbarBrand href="/">
          <img src="/img/wig.png" alt="Π"></img>
          αρατηρητήριο
        </NavbarBrand>
        <NavbarToggler onClick={ this.toggle } />

        <Collapse isOpen={ this.state.isOpen } navbar>
          <Nav className="ml-auto" navbar>
            <NavItem>
              <NavLink href="/">Αναζήτηση τιμών</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="/shops">Καταστήματα</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="/products">Προϊόντα</NavLink>
            </NavItem>
            <UserActions />
          </Nav>
        </Collapse>
      </Navbar>
    )
  }
}

export default inject('store')(observer(Header))
