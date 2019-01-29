import React, { Component } from 'react'
import { Link } from 'react-router-dom'

class Header extends Component {
  render() {
    return (
      <nav>
        <Link to='/'>Home</Link>
      </nav>
    )
  }
}

export default Header