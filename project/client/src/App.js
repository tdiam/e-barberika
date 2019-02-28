import React, { Component } from 'react'
import { Provider } from 'mobx-react'

import Header from './partials/Header'
import Main from './partials/Main'
import RootStore from './stores'

class App extends Component {
  store = new RootStore()

  render () {
    return (
      <Provider store={ this.store }>
        <div className="App">
          <Header />
          <Main />
        </div>
      </Provider>
    )
  }
}

export default App
