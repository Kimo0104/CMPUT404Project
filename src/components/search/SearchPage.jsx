import * as React from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import TopBar from '../topbar/TopBar.jsx'
import { searchForAuthors } from '../../APIRequests'
import SearchList from './SearchList.jsx';
import { Pagination, Typography } from '@mui/material';
import { QueryContext } from '../home/Home.jsx';

export default function SearchPage(props) {

    const [searchParams, setSearchParams] = useSearchParams();
    const [authors, setAuthors] = React.useState([]);
    const [numPages, setNumPages] = React.useState(0);
    const [lastQuery, setLastQuery] = React.useState('');
    const [authorsPage, setAuthorsPage] = React.useState([]);

    const { setQuery } = React.useContext(QueryContext);

    const navigate = useNavigate();
    
    let query = React.useContext(QueryContext).query;
    if (typeof(query) === "string") { query = query.split(','); }
    let page  = parseInt(searchParams.get("page"));
    let size  = parseInt(searchParams.get("size"));

    if (query === null) {
        query = "";
    }
    if (Number.isNaN(size) || size < 1) {
        // Default page size
        size = 10;
    } 
    if (Number.isNaN(page) || page < 1) {
        page = 1;
    }

    const fetchFilteredAuthors = async (query, page, size) => {
        const data = await searchForAuthors(query, page, size);

        if (page > data.numPages) {
            page = data.numPages;
        }

        setAuthors(data.authorsPage);
        setAuthorsPage(data.authorsPage.slice(0, size));
        setNumPages(parseInt(data.numPages));
        if (data.authorsPage.length == 0) {
            document.getElementById("searchtext").innerText = "No search results were found";
        }
        setLastQuery(query);
        //setSearchParams(`query=${query}&page=${page}&size=${size}`);

    }

    const handlePageChange = async (e, pageNumber) => {
        //e.preventDefault();

        let searchPath = `/search?query=${query}&page=${pageNumber}`;
        if (size !== null) {
            searchPath += `&size=${size}`;
        }

        setQuery([query[0], pageNumber]);
        localStorage.setItem("query", [query[0], pageNumber]);
        if (query !== lastQuery) {
            setLastQuery(query);
            //fetchFilteredAuthors(query[0], query[1], size);
        }
        setAuthorsPage(authors.slice((pageNumber-1)*size, pageNumber*size));

        //navigate(searchPath);
        //navigate(0);
    }

    React.useEffect(() => {
        fetchFilteredAuthors(query[0], 1, size);
        if (document.getElementById("searchtext")) {
            document.getElementById("searchtext").innerText = "Loading...";
        }
    }, [query]);

    let pagination = "";
    if (numPages != 0 && authors.length > 0) {
        pagination = <Pagination count={Math.ceil(authors.length/size)} color="secondary" onChange={handlePageChange} page={+query[1]} 
                                 style={{justifyContent: "center", display: "flex"}}/>;
    }

    return (
        <div>
            {authors.length > 0 && (query[0] == lastQuery[0] || query[0] == lastQuery)?
                <SearchList filteredAuthors={authorsPage}/>
            :
                <Typography id="searchtext" variant="h5">Loading...</Typography>   
            }
            {authors.length > 0 && numPages != 0 && (query[0] == lastQuery[0] || query[0] == lastQuery) ?
                <Pagination count={Math.ceil(authors.length/size)} color="secondary" onChange={handlePageChange} page={+query[1]} 
                style={{justifyContent: "center", display: "flex"}}/>
                :
                ""
            }   
        </div>
    );

}