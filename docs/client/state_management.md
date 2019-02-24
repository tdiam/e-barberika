# Client > State management

> To **state management** αφορά τη διαχείριση της κατάστασης ενός ή παραπάνω αντικειμένων σε μια διεπαφή χρήστη, όπως τα πεδία κειμένου, τα κουμπιά, η πολλαπλή επιλογή κλπ. Σε αυτήν την τεχνική σχεδίασης διεπαφών, η κατάσταση ενός αντικειμένου εξαρτάται από τις καταστάσεις άλλων αντικειμένων. Για παράδειγμα, ένα κουμπί θα είναι clickable μόνο όταν τα πεδία εισόδου έχουν έγκυρες τιμές, ενώ θα είναι disabled όταν τα πεδία είναι κενά ή δεν έχουν έγκυρες τιμές.
>
> [Wikipedia](https://en.wikipedia.org/wiki/State_management)

Το state management είναι πολύ εύκολο όταν αφορά μόνο ένα component, πχ. ένα κουμπί με δύο καταστάσεις on/off.

Παράδειγμα:

```javascript
class OnOff extends Component {
    state = { on: false }
    toggle = () => {
        this.setState({ on: !this.state.on })
    }
    render() {
        return (
            <button onClick={ this.toggle }>
                { this.state.on ? 'On' : 'Off' }
            </button>
        )
    }
}
```

Ωστόσο αυτό γίνεται πολύ δύσκολο όταν έχουμε να κάνουμε με παραπάνω από ένα components που πρέπει να διαχειρίζονται κοινή πληροφορία (application-level state).

Γι' αυτόν τον λόγο υπάρχουν βιβλιοθήκες state management όπως το Redux ή το MobX που χρησιμοποιούμε εμείς.

## Έννοιες

### Observables

Οποιοδήποτε αντικείμενο (object, array ή class) θέλουμε να ανήκει στο application state και να παρακολουθείται για τυχόν αλλαγές.

### Observer

Προκειμένου ένα component να ενημερώνεται αυτόματα για αλλαγές στην τιμή κάποιου observable, θα πρέπει να δηλωθεί ως observer του.

### Action

Ειδικές συναρτήσεις που αλλάζουν την κατάσταση/τιμή ενός observable με τρόπο που διασφαλίζει τη συνέπεια (consistency) των δεδομένων. Γι' αυτό πρέπει κάθε αλλαγή σε observables να γίνεται **μόνο** μέσω actions.

### Store

Συλλογή από observables και actions που αφορούν συγκεκριμένο τμήμα της εφαρμογής (πχ. Βιβλία σε εφαρμογή για βιβλιοθήκη).

Δομούνται ιεραρχικά, έχοντας ως κορυφή το root store που γίνεται διαθέσιμο σε όλα τα components και έχει ως παιδιά του τα επιμέρους stores.

## Δομή stores

`RootStore`
- `AuthStore`
- `ShopStore`
- `ProductStore`

## Χρήση

### [Γρήγορη εισαγωγή](https://mobx.js.org/intro/overview.html) από τα docs του MobX

### Παράδειγμα χρήσης: ShopListing

```javascript
import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'

class ShopListing extends Component {
    constructor(props) {
        super(props)
        this.store = this.props.store.shopStore
    }
    componentDidMount() {
        // Execute API call that will update the store state
        this.store.getShops()
    }
    render() {
        let shopItems = this.store.shops.map(shop => (
            <li key={ shop.id }>{ shop.name }</li>
        ))
        return (
            <div>
                <h2>Shops:</h2>
                <ul>
                    { shopItems }
                </ul>
            </div>
        )
    }
}

export default inject('store')(observer(ShopListing))
```

Αρχικά παρατηρούμε την τελευταία γραμμή του export, όπου εφαρμόζουμε στο component μας τους δύο εξής decorators:
- `observer`: Ώστε να παρακολουθεί τις αλλαγές στα observables που περιέχει.
- `inject('store')`: Παίρνει το store από τον Provider (βλ. `App.js`) και το εισάγει (inject) στο component ως `this.props.store`.

Για ευκολία στον constructor ορίζουμε το `this.store` του component να δείχνει στο `ShopStore` (ώστε να μην επαναλαμβάνουμε το `this.props.store.shopStore` παντού).

Μόλις γίνει [mount](https://reactjs.org/docs/react-component.html#componentdidmount) το component, καλούμε την `getShops()` (MobX action) ώστε να εκτελέσει την κλήση στο API. Εσωτερικά, αυτή θα ενημερώσει το state και θα βάλει στο `shops` τα καταστήματα που επέστρεψε ο server.

Έτσι, στην render μπορούμε να επιστρέψουμε μία λίστα με τα ονόματα των καταστημάτων.