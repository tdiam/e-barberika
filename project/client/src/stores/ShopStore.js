import { observable, action, decorate, runInAction } from 'mobx'
import Api from '../utils/api'

class ShopStore {
    constructor(root) {
        this.rootStore = root
    }

    shops = []
    pagination = { start: 0, count: 0, total: 0 }
    shop = {}
    state = 'pending' // One of 'pending' | 'done' | 'error'

    /**
     * Fetches list of shops from API and stores them in the `shops` observable.
     * Also sets the `pagination` observable.
     * 
     * @param {Object} params The query params of start, count, status and sort.
     * @returns Nothing.
     * @error On error, sets state and prints to error console.
     */
    async getShops(params) {
        this.shops = []
        this.pagination = { start: 0, count: 0, total: 0 }
        this.state = 'pending'
        try {
            const res = await Api.get('/shops/', params)
            console.log(res.data)
            const { start, count, total, shops } = res.data
            runInAction(() => {
                this.state = 'done'
                this.shops = shops
                this.pagination = { start, count, total }
            })
        } catch(err) {
            this.state = 'error'
            console.error(err)
        }
    }

    /**
     * Fetches the shop with the given id from API and stores it in the `shop` observable.
     * 
     * @param {Number} id The shop id.
     * @returns Nothing.
     * @error On error, sets state and prints to error console.
     */
    async getShop(id) {
        this.shop = {}
        this.state = 'pending'
        try {
            const res = await Api.get(`/shops/${id}/`)
            runInAction(() => {
                this.state = 'done'
                this.shop = res.data
            })
        } catch(err) {
            this.state = 'error'
            console.error(err)
        }
    }

    /**
     * Submits a POST request to create a shop with the given data and stores it in `shop`.
     * 
     * @param {Object} data The submitted data.
     * @returns Nothing.
     * @error On error, sets state and prints to error console.
     */
    async addShop(data) {
        this.shop = {}
        this.state = 'pending'
        try {
            const res = await Api.post('/shops/', data)
            runInAction(() => {
                this.state = 'done'
                this.shop = res.data
            })
        } catch(err) {
            this.state = 'error'
            console.error(err)
        }
    }

    /**
     * Submits a PATCH request to modify a shop with the given data and stores it in `shop`.
     * NOTE: PUT requests have no meaning in the context of a UI application.
     * 
     * @param {Number} id The shop id.
     * @param {Object} data The submitted data.
     * @returns Nothing.
     * @error On error, sets state and prints to error console.
     */
    async editShop(id, data) {
        this.shop = {}
        this.state = 'pending'
        try {
            const res = await Api.patch(`/shops/${id}/`, data)
            runInAction(() => {
                this.state = 'done'
                this.shop = res.data
            })
        } catch(err) {
            this.state = 'error'
            console.error(err)
        }
    }

    /**
     * Deletes the shop with the given id.
     * 
     * @param {Number} id The shop id.
     * @returns Nothing.
     * @error On error, sets state and prints to error console.
     */
    async deleteShop(id) {
        this.shop = {}
        this.state = 'pending'
        try {
            await Api.delete(`/shops/${id}/`)
            runInAction(() => {
                this.state = 'done'
            })
        } catch(err) {
            this.state = 'error'
            console.error(err)
        }
    }
}
decorate(ShopStore, {
    shops: observable,
    shop: observable,
    state: observable,
    getShops: action,
    getShop: action,
    addShop: action,
    editShop: action,
    deleteShop: action,
})

export default ShopStore