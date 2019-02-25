# Client > StateHandler

Όταν ένα component χρειάζεται να περιέχει πληροφορίες που έρχονται από το API, το κάνει μέσω των [stores](state_management.md).

Οι κλήσεις ωστόσο στο API δεν πετυχαίνουν πάντα και δεν είναι σίγουρο ότι θα έχουν εκτελεστεί πριν γίνει το πρώτο render. Γι' αυτόν τον λόγο κάθε store έχει ένα state που δείχνει σε τι κατάσταση βρίσκεται. Αυτό μπορεί να είναι ένα από τα ακόλουθα:

* `pending`: Δεν έχει ολοκληρώσει την κλήση API ακόμη.
* `done`: Η κλήση ήταν επιτυχής και τα δεδομένα είναι έτοιμα.
* `unauthorized`: Η κλήση απέτυχε επειδή ο χρήστης δεν έχει αρκετά δικαιώματα.
* `error`: Η κλήση απέτυχε για άλλον λόγο.

Άρα πρέπει με κάποιον τρόπο να ελέγχουμε σε τι κατάσταση είναι το store, ώστε να κάνουμε το κατάλληλο render. Αυτή η διαδικασία απλοποιείται με τον `StateHandler`.

## Τι κάνει ο `StateHandler`;

Εσωτερικά, η λειτουργία του είναι πολύ απλή. Παίρνει ως είσοδο (props) το `state` και ένα component. Αν το `state` είναι ίσο με `done`, τότε κάνει render το component. Αλλιώς δείχνει μήνυμα σφάλματος.

#### (Ψευδο)κώδικας
```javascript
class StateHandler extends Component {
    render() {
        if(this.props.state === 'done') return this.props.children
        if(this.props.state === 'pending') return this.props.ifPending
        if(this.props.state === 'error') return this.props.ifError
        if(this.props.state === 'unauthorized') return this.props.ifUnauthorized
    }
}
```

Τα `ifPending`, `ifError` και `ifUnauthorized` είναι props με default τιμές αλλά μπορούν να τροποποιηθούν αν περάσουμε δικά μας components στη θέση τους.

## Παράδειγμα χρήσης 1
```javascript
import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

class Shop1 extends Component {
    constructor(props) {
        super(props)
        this.store = this.props.store.shopStore
    }
    componentDidMount() {
        // Execute API call to get shop with ID 1
        this.store.getShop(1)
    }
    render() {
        const shop = this.store.shop
        return (
            <StateHandler state={ this.store.state }>
                <div>
                    <h2>Shop { shop.name }</h2>
                    <h4>Address: { shop.address }</h4>
                </div>
            </StateHandler>
        )
    }
}

export default inject('store')(observer(Shop1))
```

Το παραπάνω component θα εμφανίσει το κατάστημα 1 αν το `state` είναι `done`, θα εμφανίσει μήνυμα σφάλματος αν το `state` γίνει `error` κ.ο.κ.

## Παράδειγμα χρήσης 2

Αν θέλουμε να εμφανίσουμε προσαρμοσμένο μήνυμα σφάλματος, τότε μπορούμε να περάσουμε δικό μας component στο prop `ifError`.

```javascript
// ...
    render() {
        const shop = this.store.shop
        return (
            <StateHandler state={ this.store.state } ifError={ <strong>BIG FAIL</strong> }>
                <div>
                    <h2>Shop { shop.name }</h2>
                    <h4>Address: { shop.address }</h4>
                </div>
            </StateHandler>
        )
    }
// ...
```

## Παράδειγμα χρήσης 3

Ας δοκιμάσουμε να εμφανίσουμε και τα tags του καταστήματος στην render μας.

```javascript
// ...
    render() {
        const shop = this.store.shop
        return (
            <StateHandler state={ this.store.state } ifError={ <strong>BIG FAIL</strong> }>
                <div>
                    <h2>Shop { shop.name }</h2>
                    <h4>Address: { shop.address }</h4>
                    <ul>
                        { shop.tags.map(tag => (
                            <li>{ tag }</li>
                        ))}
                    </ul>
                </div>
            </StateHandler>
        )
    }
// ...
```

Θα παρατηρήσουμε ότι σκάει με *shop.tags is undefined*.

#### Τι φταίει;

Ο λόγος είναι ότι το React πριν περάσει το child component του καταστήματος στον `StateHandler` πρέπει να κάνει evaluate τις τιμές που χρησιμοποιεί (`shop.name`, `shop.address`, `shop.tags`), και αυτό όχι μόνο όταν το `state` είναι `done` αλλά **σε κάθε περίπτωση**.

Μέχρι εδώ δεν είχαμε πρόβλημα, αφού όταν πχ. το `state` ήταν `error`, το `shop` ήταν `{}` και τα `shop.name`, `shop.address` ήταν απλά `undefined`.

Τώρα όμως δεν μπορούμε να κάνουμε `map` σε `undefined` και σκάει.

#### Πώς λύνεται;

Αντί να περάσουμε το component ως παιδί στον `StateHandler`, μπορούμε να κάνουμε lazy evaluation δίνοντας αντ' αυτού μία συνάρτηση που επιστρέφει το component.

#### Τελικός κώδικας

```javascript
// ...
    render() {
        const shop = this.store.shop
        return (
            <StateHandler state={ this.store.state } ifError={ <strong>BIG FAIL</strong> }>
            { /* συνάρτηση που επιστρέφει component */ }
            {() => (
                <div>
                    <h2>Shop { shop.name }</h2>
                    <h4>Address: { shop.address }</h4>
                    <ul>
                        { shop.tags.map(tag => (
                            <li>{ tag }</li>
                        ))}
                    </ul>
                </div>
            )}
            </StateHandler>
        )
    }
// ...
```