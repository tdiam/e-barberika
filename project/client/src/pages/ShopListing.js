import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import MaterialTable from 'material-table'

class ShopListing extends Component {
    constructor(props) {
        super(props)
        this.root = this.props.store
        this.store = this.props.store.shopStore

        this.columns = [{
            title: 'Όνομα καταστήματος',
            field: 'name',
        }, {
            title: 'Διεύθυνση',
            field: 'address',
        }, {
            title: 'Κρυμμένο',
            field: 'withdrawn',
            type: 'boolean'
        }]

        this.actions = [{
            icon: 'delete',
            orig: this,
            tooltip: 'Διαγραφή Καταστήματος',
            onClick: this.called
        }]
    }

    async loadShops() {
        // Execute API call that will update the store state
        // NOTE: not too good if we have too many shops
        await this.store.getShops({count:0})
        await this.store.getShops({count:this.store.pagination.total, status: 'ALL'})
    }

    async componentDidMount() {
        await this.loadShops()
    }

    async called(e, row) {
        console.log(this)
        console.log("Clicked on", row.name)

        await this.orig.store.deleteShop(row.id)
        await this.orig.loadShops()
    }

    render() {
        if (! this.root.isLoggedIn) {
            return (
                <div>
                    You must log in
                </div>
            )
        }
        if (this.store.state === 'done') {
            return (
                <MaterialTable 
                    data={this.store.shops}
                    columns={this.columns}
                    title={"Shops"}
                    actions={this.actions}
                    options={{
                        actionsColumnIndex: -1,
                        pageSize: 10
                    }}
                />
            )
        }
        return (
            <div>
                <p>pending</p>
            </div>
        )
    }
}

export default inject('store')(observer(ShopListing))