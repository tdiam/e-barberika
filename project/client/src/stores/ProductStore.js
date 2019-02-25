import { observable, action, decorate, runInAction } from 'mobx'

import Api from '../utils/Api'
import { handleError } from './helpers'

class ProductStore {
    constructor(root) {
        this.rootStore = root
        this.handleError = handleError.bind(this)
    }

    products = []
    pagination = { start: 0, count: 0, total: 0 }
    product = {}
    state = 'pending' // One of 'pending' | 'done' | 'unauthorized' | 'error'

    /**
     * Fetches list of products from API and stores them in the `products` observable.
     * Also sets the `pagination` observable.
     * 
     * @param {Object} params The query params of start, count, status and sort.
     * @returns Nothing.
     */
    async getProducts(params) {
        this.state = 'pending'
        this.products = []
        this.pagination = { start: 0, count: 0, total: 0 }
        try {
            const res = await Api().get('/products/', params)
            const { start, count, total, products } = res.data
            runInAction(() => {
                this.state = 'done'
                this.products = products
                this.pagination = { start, count, total }
            })
        } catch(err) {
            this.handleError(err)
        }
    }

    /**
     * Fetches the product with the given id from API and stores it in the `product` observable.
     * 
     * @param {Number} id The product id.
     * @returns Nothing.
     */
    async getProduct(id) {
        this.product = {}
        this.state = 'pending'
        try {
            const res = await Api().get(`/products/${id}/`)
            runInAction(() => {
                this.state = 'done'
                this.product = res.data
            })
        } catch(err) {
            this.handleError(err)
        }
    }

    /**
     * Submits a POST request to create a product with the given data and stores it in `product`.
     * 
     * @param {Object} data The submitted data.
     * @returns Nothing.
     */
    async addProduct(data) {
        this.product = {}
        this.state = 'pending'
        try {
            const res = await Api({ token: this.rootStore.user.token }).post('/products/', data)
            runInAction(() => {
                this.state = 'done'
                this.product = res.data
            })
        } catch(err) {
            this.handleError(err)
        }
    }

    /**
     * Submits a PATCH request to modify a product with the given data and stores it in `product`.
     * NOTE: PUT requests have no meaning in the context of a UI application.
     * 
     * @param {Number} id The product id.
     * @param {Object} data The submitted data.
     * @returns Nothing.
     */
    async editProduct(id, data) {
        this.product = {}
        this.state = 'pending'
        try {
            const res = await Api({ token: this.rootStore.user.token }).patch(`/products/${id}/`, data)
            runInAction(() => {
                this.state = 'done'
                this.product = res.data
            })
        } catch(err) {
            this.handleError(err)
        }
    }

    /**
     * Deletes the product with the given id.
     * 
     * @param {Number} id The product id.
     * @returns Nothing.
     */
    async deleteProduct(id) {
        this.product = {}
        this.state = 'pending'
        try {
            await Api({ token: this.rootStore.user.token }).delete(`/products/${id}/`)
            runInAction(() => {
                this.state = 'done'
            })
        } catch(err) {
            this.handleError(err)
        }
    }
}
decorate(ProductStore, {
    products: observable,
    product: observable,
    state: observable,
    getProducts: action,
    getProduct: action,
    addProduct: action,
    editProduct: action,
    deleteProduct: action,
})

export default ProductStore