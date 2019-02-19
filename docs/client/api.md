# Client > API

Όλες οι πιθανές κλήσεις στο API έχουν υλοποιηθεί ως actions στα αντίστοιχα stores και μπορούν να θεωρηθούν ως black box.

Αυτό που πρέπει να γνωρίζει κάποιος είναι ότι:
* Οι κλήσεις εκτελούνται ασύγχρονα.  
  > **Reading material:**
  >
  >[Getting to know asynchronous JavaScript: Callbacks, Promises and Async/Await](https://medium.com/codebuddies/getting-to-know-asynchronous-javascript-callbacks-promises-and-async-await-17e0673281ee) του Sebastian Lindström
* Ο χειρισμός των errors γίνεται στο επίπεδο των actions μέσω try-catch ως εξής:  
  1. Όλα τα errors τυπώνονται στο `console.error`.
  2. Αν συμβεί error, το observable `state` του εκάστοτε store παίρνει την τιμή `'error'` ή `'unauthorized'` (αν επιστράφηκε response 401).

  Επομένως, κάθε φορά μετά από μία κλήση API θα πρέπει να ελέγχεται το αντίστοιχο `state` για χειρισμό πιθανών errors.

### Λίστα

* `ShopStore`  
  - `getShops({ start, count, status, sort })`
  - `getShop(id)`
  - `addShop({ name, address, lat, lng, tags })`
  - `editShop(id, { name, address, lat, lng, tags })`
  - `deleteShop(id)`
* `ProductStore`
  - `getProducts({ start, count, status, sort })`
  - `getProduct(id)`
  - `addProduct({ name, description, category, tags })`
  - `editProduct(id, { name, address, category, tags })`
  - `deleteProduct(id)`
* `PriceStore`
  - `getPrices(params)`  
    Όπου οι υποστηριζόμενες παράμετροι είναι οι εξής:
    ```javascript
    params = {
        start, count,
        geoLng, geoLat, geoDist,
        dateFrom, dateTo,
        shops,
        products,
        tags,
        sort
    }
    ```
  - `addPrice({ price, dateFrom, dateTo, productId, shopId })`
* `AuthStore`
  - `authenticate(username, password)`
  - `register(username, password)`
  - `logout()`

Καθεμία από τις παραπάνω κλήσεις ενημερώνει τα πεδία του αντίστοιχου store με τα δεδομένα που έλαβε από τον server. Για παράδειγμα η `getShops` θα βάλει στο `ShopStore.shops` τη λίστα με τα καταστήματα. Η `editProduct` θα βάλει στο `ProductStore.product` το τροποποιημένο προϊόν.

Οι `deleteShop, deleteProduct, addPrice` δεν αποθηκεύουν κάτι.

Το `AuthStore` από την άλλη αποθηκεύει τα δεδομένα του στο πεδίο `user` του `RootStore` ώστε να είναι διαθέσιμες σε όλα τα stores οι πληροφορίες `user.username` και `user.token`.