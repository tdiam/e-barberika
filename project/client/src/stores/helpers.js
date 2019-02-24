import { runInAction } from 'mobx'

/**
 * Common error handler for our stores that sets state to 'unauthorized' or 'error'.
 *
 * NOTE: The function has to be bound to the store class in order for the
 * `this.state` assignments to work correctly.
 * 
 * @param {Error} error
 * @example
 * import { handleError } from './helpers'
 * 
 * class MyStore {
 *     constructor() {
 *         this.handleError = handleError.bind(this)
 *     }
 * }
 */
export function handleError(error) {
    console.error(error)
    if(error.response && error.response.status === 401) {
        runInAction(() => {
            this.state = 'unauthorized'
        })
    } else {
        runInAction(() => {
            this.state = 'error'
        })
    }
}