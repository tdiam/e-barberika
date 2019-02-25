import React, { Component } from 'react'
import { Route, Switch } from 'react-router-dom'

import Home from '../pages/Home'
import LoginForm from '../pages/LoginForm'
import ShopListing from '../pages/ShopListing'
import Shop from '../pages/Shop'
import AddShop from '../pages/AddShop'
import MapDemo from '../pages/MapDemo'
import SignupForm from '../pages/SignupForm'
import Page404 from '../pages/Page404'

class Main extends Component {
    render() {
        return (
            <Switch>
                <Route exact path="/" component={ Home } />
                <Route exact path="/login" component={ LoginForm } />
                <Route exact path="/shops" component={ ShopListing } />
                <Route path="/shops/:id" component={ Shop } />
                <Route exact path="/shops/add" component={ AddShop } />
                <Route exact path="/map" component={ MapDemo } />
                <Route exact path="/signup" component={ SignupForm } />
                <Route component={ Page404 } />
            </Switch>
        )
    }
}

export default Main