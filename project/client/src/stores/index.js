import { decorate, observable, action, computed } from 'mobx'
import AuthStore from './AuthStore'
import ShopStore from './ShopStore'
import ProductStore from './ProductStore'
import PriceStore from './PriceStore'

class RootStore {
  constructor () {
    this.authStore = new AuthStore(this)
    this.shopStore = new ShopStore(this)
    this.productStore = new ProductStore(this)
    this.priceStore = new PriceStore(this)
    this.setUserFromStorage()
  }

  user = {
    username: '',
    token: '',
  }

  get isLoggedIn () {
    return !!this.user.token
  }

  get userOrGuest () {
    return this.isLoggedIn ? this.user.username : 'Ανώνυμος'
  }

  /**
   * Checks to see if credentials have been stored in localStorage.
   * If so, "logs in" user.
   */
  setUserFromStorage () {
    let username = localStorage.getItem('username'),
        token = localStorage.getItem('token')
    if (username != null && token != null) {
      this.user = { username, token }
    }
  }

  setUser ({ username, token }) {
    this.user = { username, token }
    localStorage.setItem('username', username)
    localStorage.setItem('token', token)
  }

  clearUser () {
    this.user = { username: '', token: '' }
    localStorage.removeItem('username')
    localStorage.removeItem('token')
  }
}
decorate(RootStore, {
  user: observable,
  isLoggedIn: computed,
  userOrGuest: computed,
  setUser: action,
  setUserFromStorage: action,
  clearUser: action,
})

export default RootStore
