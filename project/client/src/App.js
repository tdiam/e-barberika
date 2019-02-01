import React, { Component } from 'react'
import { Provider } from 'mobx-react'

import Header from './partials/Header'
import Main from './partials/Main'
import RootStore from './stores'

class App extends Component {
  render() {
    const store = new RootStore()
    return (
      <Provider store={store}>
        <div className="App">
          <Header />
          <Main />
        </div>
      </Provider>
    )
  }
}

export default App
