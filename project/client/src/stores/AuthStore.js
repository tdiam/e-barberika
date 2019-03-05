import { observable, action, decorate, runInAction } from 'mobx'

import Api from '../utils/Api'
import { handleError } from './helpers'

class AuthStore {
  constructor (root) {
    this.rootStore = root
    this.handleError = handleError.bind(this)
  }

  state = 'pending' // One of 'pending' | 'done' | 'unauthorized' | 'error'

  setState(state) {
    this.state = state
  }

  /**
   * Resets state to pending
   */
  resetState() {
    this.state = 'pending'
  }

  /**
   * Authenticate with given credentials and store token if successful
   *
   * @param {String} username
   * @param {String} password
   * @returns Nothing
   * @error On error, sets state and prints to error console.
   */
  async authenticate (username, password) {
    this.state = 'pending'
    this.rootStore.clearUser()
    try {
      const res = await Api().post('/login/', { username, password })
      const { token } = res.data
      runInAction(() => {
        this.state = 'done'
      })
      this.rootStore.setUser({ username, token })
    } catch (err) {
      this.handleError(err)
    }
  }

  /**
   * Register user
   *
   * @param {String} username
   * @param {String} password
   * @returns Nothing
   * @error On error, sets state and prints to error console.
   */
  async register (username, password) {
    this.state = 'pending'
    try {
      await Api().post('/register/', { username, password })
      runInAction(() => {
        this.state = 'done'
      })
    } catch (err) {
      this.handleError(err)
    }
  }

  /**
   * Logout user if there is one logged in and clear user if successful
   *
   * @returns Nothing
   * @error On error, sets state and prints to error console.
   */
  async logout () {
    this.state = 'pending'
    const token = this.rootStore.user.token
    if (!token) {
      this.state = 'done'
      console.info('No user was logged in')
      return
    }
    try {
      await Api({ token }).post('/logout/', {})
      runInAction(() => {
        this.state = 'done'
      })
      this.rootStore.clearUser()
    } catch (err) {
      this.handleError(err)
    }
  }
}
decorate(AuthStore, {
  state: observable,
  setState: action,
  resetState: action,
  authenticate: action,
  register: action,
  logout: action,
})

export default AuthStore
