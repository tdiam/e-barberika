import { observable, action, decorate, runInAction } from 'mobx'

import Api from '../utils/Api'
import { handleError } from './helpers'

class ShopStore {
  constructor (root) {
    this.rootStore = root
    this.handleError = handleError.bind(this)
  }

  shops = []
  pagination = { start: 0, count: 0, total: 0 }
  shop = {}
  state = 'pending' // One of 'pending' | 'done' | 'unauthorized' | 'error'

  /**
   * Fetches list of shops from API and stores them in the `shops` observable.
   * Also sets the `pagination` observable.
   *
   * @param {Object} params The query params of start, count, status and sort.
   * @returns Nothing.
   */
  async getShops (params) {
    this.state = 'pending'
    this.shops = []
    this.pagination = { start: 0, count: 0, total: 0 }
    try {
      const res = await Api().get('/shops/', params)
      const { start, count, total, shops } = res.data
      runInAction(() => {
        this.state = 'done'
        this.shops = shops
        this.pagination = { start, count, total }
      })
    } catch (err) {
      this.handleError(err)
    }
  }

  /**
   * Fetches the shop with the given id from API and stores it in the `shop` observable.
   *
   * @param {Number} id The shop id.
   * @returns Nothing.
   */
  async getShop (id) {
    this.shop = {}
    this.state = 'pending'
    try {
      const res = await Api().get(`/shops/${id}/`)
      runInAction(() => {
        this.state = 'done'
        this.shop = res.data
      })
    } catch (err) {
      this.handleError(err)
    }
  }

  /**
   * Submits a POST request to create a shop with the given data and stores it in `shop`.
   *
   * @param {Object} data The submitted data.
   * @returns Nothing.
   */
  async addShop (data) {
    this.shop = {}
    this.state = 'pending'
    try {
      const res = await Api({ token: this.rootStore.user.token }).post('/shops/', data)
      runInAction(() => {
        this.state = 'done'
        this.shop = res.data
      })
    } catch (err) {
      this.handleError(err)
    }
  }

  /**
   * Submits a PATCH request to modify a shop with the given data and stores it in `shop`.
   * NOTE: PUT requests have no meaning in the context of a UI application.
   *
   * @param {Number} id The shop id.
   * @param {Object} data The submitted data.
   * @returns Nothing.
   */
  async editShop (id, data) {
    this.shop = {}
    this.state = 'pending'
    try {
      const res = await Api({ token: this.rootStore.user.token }).patch(`/shops/${id}/`, data)
      runInAction(() => {
        this.state = 'done'
        this.shop = res.data
      })
    } catch (err) {
      this.handleError(err)
    }
  }

  /**
   * Deletes the shop with the given id.
   *
   * @param {Number} id The shop id.
   * @returns Nothing.
   */
  async deleteShop (id) {
    this.shop = {}
    this.state = 'pending'
    try {
      await Api({ token: this.rootStore.user.token }).delete(`/shops/${id}/`)
      runInAction(() => {
        this.state = 'done'
      })
    } catch (err) {
      this.handleError(err)
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
