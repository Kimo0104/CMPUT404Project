import * as React from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import TopBar from '../topbar/TopBar.jsx'
import { searchForAuthors } from '../../APIRequests'
import SearchList from './SearchList.jsx';
import { Pagination } from '@mui/material';

export default function SearchPage() {

    const [searchParams, setSearchParams] = useSearchParams();
    const [authors, setAuthors] = React.useState([]);
    const [numPages, setNumPages] = React.useState(0);

    const navigate = useNavigate();
    
    let query = searchParams.get("query");
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
            page = data.numPages
        }

        setAuthors(data.authorsPage);
        setNumPages(parseInt(data.numPages));
        setSearchParams(`query=${query}&page=${page}&size=${size}`);

    }

    const handlePageChange = async (e, pageNumber) => {
        //e.preventDefault();

        let searchPath = `/search?query=${query}&page=${pageNumber}`;
        if (size !== null) {
            searchPath += `&size=${size}`;
        }

        navigate(searchPath);
        navigate(0);
    }

    React.useEffect(() => {
        fetchFilteredAuthors(query, page, size);
    }, []);

    let pagination = "";
    if (numPages != 0) {
        pagination = <Pagination count={numPages} color="secondary" onChange={handlePageChange} page={page} 
                                 style={{justifyContent: "center", display: "flex"}}/>;
    }

    return (
        <div>
            <TopBar />
            <SearchList filteredAuthors={authors}/>
            {pagination}
        </div>
    );

}