import { decorate, observable, action, computed } from 'mobx'
import AuthStore from './AuthStore'
import ShopStore from './ShopStore'
import ProductStore from './ProductStore'

class RootStore {
    constructor() {
        this.authStore = new AuthStore(this)
        this.shopStore = new ShopStore(this)
        this.productStore = new ProductStore(this)
    }

    user = {
        username: '',
        token: '',
    }

    get isLoggedIn() {
        return !!this.user.token
    }

    get userOrGuest() {
        return this.isLoggedIn ? this.user.username : 'Guest'
    }

    setUser({ username, token }) {
        this.user = { username, token }
    }

    clearUser() {
        this.user = { username: '', token: '' }
    }
}
decorate(RootStore, {
    user: observable,
    isLoggedIn: computed,
    userOrGuest: computed,
    setUser: action,
    clearUser: action,
})

export default RootStore