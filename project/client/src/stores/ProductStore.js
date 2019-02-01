import { observable, action, decorate, runInAction } from 'mobx'
import Api from '../utils/api'

class ProductStore {
    constructor(root) {
        this.rootStore = root
    }

    products = []
    pagination = { start: 0, count: 0, total: 0 }
    product = {}
    state = 'pending' // One of 'pending' | 'done' | 'error'

    /**
     * Fetches list of products from API and stores them in the `products` observable.
     * Also sets the `pagination` observable.
     * 
     * @param {Object} params The query params of start, count, status and sort.
     * @returns Nothing.
     * @error On error, sets state and prints to error console.
     */
    async getProducts(params) {
        this.products = []
        this.pagination = { start: 0, count: 0, total: 0 }
        this.state = 'pending'
        try {
            const res = await Api.get('/products/', params)
            const { start, count, total, products } = res.data
            runInAction(() => {
                this.state = 'done'
                this.products = products
                this.pagination = { start, count, total }
            })
        } catch(err) {
            this.state = 'error'
            console.error(err)
        }
    }

    /**
     * Fetches the product with the given id from API and stores it in the `product` observable.
     * 
     * @param {Number} id The product id.
     * @returns Nothing.
     * @error On error, sets state and prints to error console.
     */
    async getProduct(id) {
        this.product = {}
        this.state = 'pending'
        try {
            const res = await Api.get(`/products/${id}/`)
            runInAction(() => {
                this.state = 'done'
                this.product = res.data
            })
        } catch(err) {
            this.state = 'error'
            console.error(err)
        }
    }

    /**
     * Submits a POST request to create a product with the given data and stores it in `product`.
     * 
     * @param {Object} data The submitted data.
     * @returns Nothing.
     * @error On error, sets state and prints to error console.
     */
    async addProduct(data) {
        this.product = {}
        this.state = 'pending'
        try {
            const res = await Api.post('/products/', data)
            runInAction(() => {
                this.state = 'done'
                this.product = res.data
            })
        } catch(err) {
            this.state = 'error'
            console.error(err)
        }
    }

    /**
     * Submits a PATCH request to modify a product with the given data and stores it in `product`.
     * NOTE: PUT requests have no meaning in the context of a UI application.
     * 
     * @param {Number} id The product id.
     * @param {Object} data The submitted data.
     * @returns Nothing.
     * @error On error, sets state and prints to error console.
     */
    async editProduct(id, data) {
        this.product = {}
        this.state = 'pending'
        try {
            const res = await Api.patch(`/products/${id}/`, data)
            runInAction(() => {
                this.state = 'done'
                this.product = res.data
            })
        } catch(err) {
            this.state = 'error'
            console.error(err)
        }
    }

    /**
     * Deletes the product with the given id.
     * 
     * @param {Number} id The product id.
     * @returns Nothing.
     * @error On error, sets state and prints to error console.
     */
    async deleteProduct(id) {
        this.product = {}
        this.state = 'pending'
        try {
            await Api.delete(`/products/${id}/`)
            runInAction(() => {
                this.state = 'done'
            })
        } catch(err) {
            this.state = 'error'
            console.error(err)
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