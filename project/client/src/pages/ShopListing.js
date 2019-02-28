import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import MaterialTable  from 'material-table'
import Popup from 'reactjs-popup';

class ShopListing extends Component {
    constructor(props) {
        super(props)
        this.root = this.props.store
        this.store = this.props.store.shopStore

        this.state = {
            modalOpen : false
        }

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
            this: this,
            onClick: this.editOnClick,
            icon: 'edit',
            name: 'Επεξεργασία καταστήματος'
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

    async editOnClick(e, rowData) {
        this.this.store.getShop(rowData.id)
        this.this.openModal()
    }

    openModal() {
        this.setState({
            modalOpen: true
        })
    }

    closeModal() {
        this.setState({
            modalOpen: false
        })
    }

    render() {
        //DEBUG
        // if (! this.root.isLoggedIn) {
        //     return (
        //         <div>
        //             You must log in
        //         </div>
        //     )
        // }
        if (this.store.state === 'done') {
            return (
                <>
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
                <Popup
                    open={this.state.modalOpen}
                    onClose={() => this.closeModal()} >
                    
                    <div>{this.store.shop.id}</div>
                    <div>{this.store.shop.name}</div> 
                    <div>{this.store.shop.address}</div>
                    <div>{this.store.shop.tags}</div>

                </Popup>
                </>
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
