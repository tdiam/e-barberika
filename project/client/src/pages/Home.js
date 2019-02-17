import React, { Component } from 'react'
import SearchBar from '../components/SearchBar';
// import SearchField from 'react-search-field';
import SearchResults from '../components/SearchResults';
import SearchFilters from '../components/SearchFilters';


class Home extends Component {
    
    state = {
        query: '',
        filters: {}
    }

    setQuery = (query) => {
        console.log(query)
        this.setState({ query })
    }

    setFilters = (filters) => {
        this.setState({ filters })
    }

    showFilters = () => {
        return this.state.query !== ''
    }

    render() {
        return (
            <React.Fragment>
                <div>Welcome to Asoures!</div>
                <SearchBar setQuery={ this.setQuery } />
                <SearchFilters
                    display={ /* this.showFilters() */ false }
                    setFilters={ this.setFilters } 
                />
                <SearchResults  
                    query={ this.state.query }
                    filters={ this.state.filters }
                />
            </React.Fragment>
        )
    }
}

export default Home