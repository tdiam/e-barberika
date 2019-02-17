import React, { Component } from 'react'
import { Route } from 'react-router-dom'

import Home from '../pages/Home'
import LoginForm from '../pages/LoginForm'
import ShopListing from '../pages/ShopListing'
import AddShop from '../pages/AddShop'
import MapDemo from '../pages/MapDemo'
import SignupForm from '../pages/SignupForm';

class Main extends Component {
    render() {
        return (
            <>
                <Route exact path="/" component={ Home } />
                <Route exact path="/login" component={ LoginForm } />
                <Route exact path="/shops" component={ ShopListing } />
                <Route exact path="/shops/add" component={ AddShop } />
                <Route exact path="/map" component={ MapDemo } />
                <Route exact path="/signup" component={ SignupForm } />
            </>
        )
    }
}

export default Main