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
        setNumPages(parseInt(data.numPages));
        if (data.authorsPage.length == 0) {
            document.getElementById("searchtext").innerText = "No search results were found";
        }
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
        fetchFilteredAuthors(query[0], query[1], size);

        //navigate(searchPath);
        //navigate(0);
    }

    React.useEffect(() => {
        fetchFilteredAuthors(query[0], query[1], size);
    }, [query]);

    let pagination = "";
    if (numPages != 0 && authors.length > 0) {
        pagination = <Pagination count={numPages} color="secondary" onChange={handlePageChange} page={+query[1]} 
                                 style={{justifyContent: "center", display: "flex"}}/>;
    }

    return (
        <div>
            {authors.length > 0 ?
                <SearchList filteredAuthors={authors}/>
            :
                <Typography id="searchtext" variant="h3">Loading...</Typography>   
            }
            {pagination}
        </div>
    );

}