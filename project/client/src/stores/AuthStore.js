import { observable, action, decorate, runInAction } from 'mobx'

import Api from '../utils/Api'
import { handleError } from './helpers'

class AuthStore {
    constructor(root) {
        this.rootStore = root
        this.handleError = handleError.bind(this)
    }

    state = 'done' // One of 'pending' | 'done' | 'unauthorized' | 'error'

    /**
     * Authenticate with given credentials and store token if successful
     * 
     * @param {String} username
     * @param {String} password
     * @returns Nothing
     * @error On error, sets state and prints to error console.
     */
    async authenticate(username, password) {
        this.state = 'pending'
        this.rootStore.clearUser()
        try {
            const res = await Api().post('/login/', { username, password })
            const { token } = res.data
            runInAction(() => {
                this.state = 'done'
            })
            this.rootStore.setUser({ username, token })
        } catch(err) {
            this.handleError(err)
        }
    }
}
decorate(AuthStore, {
    state: observable,
    authenticate: action,
})

export default AuthStore