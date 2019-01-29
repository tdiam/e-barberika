import React, { Component } from 'react'
import { Route } from 'react-router-dom'
import Home from '../pages/Home'

class Main extends Component {
  render() {
    return (
      <>
        <Route exact path='/' component={Home} />
      </>
    )
  }
}

export default Main