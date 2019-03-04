import React, { Component } from 'react'
import { Route, Switch } from 'react-router-dom'
import { Container } from 'reactstrap'

import Home from '../pages/Home'
import LoginForm from '../pages/LoginForm'
import SignupForm from '../pages/SignupForm'
import ShopListing from '../pages/ShopListing'
import Shop from '../pages/Shop'
import ProductListing from '../pages/ProductListing'
import Product from '../pages/Product'
import PriceAdd from '../pages/PriceAdd'
import Page404 from '../pages/Page404'

class Main extends Component {
  render () {
    return (
      <Container fluid tag="main">
        <Switch>
          <Route exact path='/' component={Home} />
          <Route exact path='/login' component={LoginForm} />
          <Route exact path='/shops' component={ShopListing} />
          <Route path='/shops/:id' component={Shop} />
          <Route exact path='/products' component={ProductListing} />
          <Route path='/products/:id' component={Product} />
          <Route exact path='/price/add' component={PriceAdd} />
          <Route exact path='/signup' component={SignupForm} />
          <Route component={ Page404 } />
        </Switch>
      </Container>
    )
  }
}

export default Main
