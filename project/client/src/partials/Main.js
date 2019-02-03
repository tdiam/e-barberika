import React, { Component } from 'react'
import { Route } from 'react-router-dom'

import Home from '../pages/Home'
import LoginForm from '../pages/LoginForm'
import ShopListing from '../pages/ShopListing'
import AddShop from '../pages/AddShop'

class Main extends Component {
    render() {
        return (
            <>
                <Route exact path="/" component={ Home } />
                <Route exact path="/login" component={ LoginForm } />
                <Route exact path="/shops" component={ ShopListing } />
                <Route exact path="/shops/add" component={ AddShop } />
            </>
        )
    }
}

export default Main