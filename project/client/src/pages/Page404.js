import React, { Component } from 'react'

import { Link } from 'react-router-dom'

class Page404 extends Component {
    render() {
        return (
            <div>
                <h1>Page Not found</h1>
                <p> Page not found! <Link to="/">Back to safety</Link></p>
            </div>
        )
    }
}

export default Page404