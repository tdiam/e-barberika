import ShopStore from './ShopStore'
import ProductStore from './ProductStore'

class RootStore {
    constructor() {
        this.shopStore = new ShopStore(this)
        this.productStore = new ProductStore(this)
    }
}

export default RootStore