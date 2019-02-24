import { observable, action, decorate, runInAction } from 'mobx'

import Api from '../utils/Api'
import { handleError } from './helpers'

class PriceStore {
    constructor(root) {
        this.rootStore = root
        this.handleError = handleError.bind(this)
    }

    prices = []
    pagination = { start: 0, count: 0, total: 0 }
    state = 'done' // One of 'pending' | 'done' | 'unauthorized' | 'error'

    /**
     * Fetches list of prices from API and stores them in the `prices` observable.
     * Also sets the `pagination` observable.
     * 
     * @param {Object} params The query params: {
     *     start, count,
     *     geoLng, geoLat, geoDist,
     *     dateFrom, dateTo,
     *     shops,
     *     products,
     *     tags,
     *     sort
     * }
     * @returns Nothing.
     */
    async getPrices(params) {
        this.state = 'pending'
        this.prices = []
        this.pagination = { start: 0, count: 0, total: 0 }
        try {
            const res = await Api().get('/prices/', params)
            const { start, count, total, prices } = res.data
            runInAction(() => {
                this.state = 'done'
                this.prices = prices
                this.pagination = { start, count, total }
            })
        } catch(err) {
            this.handleError(err)
        }
    }

    /**
     * Submits a POST request to add a price with the given data.
     * 
     * @param {Object} data The submitted data: { price, dateFrom, dateTo, productId, shopId }
     * @returns Nothing.
     */
    async addPrice(data) {
        this.state = 'pending'
        try {
            await Api({ token: this.rootStore.user.token }).post('/prices/', data)
            runInAction(() => {
                this.state = 'done'
            })
        } catch(err) {
            this.handleError(err)
        }
    }
}
decorate(PriceStore, {
    prices: observable,
    getPrices: action,
    addPrice: action,
})

export default PriceStore