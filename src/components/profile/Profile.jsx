import * as React from 'react';
import TopBar from '../topbar/TopBar.jsx'
import { getAuthor } from '../../APIRequests'
import { borderLeft } from '@mui/system';
import { Button, Typography } from '@mui/material';
import { useLocation } from 'react-router-dom';


export default function Profile(props)  {

    const location = useLocation();

    let userId = props.userId !== null ? props.userId : location.userId ;
    
    let authorId = window.location.pathname.split("/").at(-1)
    const [author, setAuthor] = React.useState({});

    const fetchAuthor = async () => {
        const author = await getAuthor(authorId);
        setAuthor(author);
    };

    React.useEffect(() => {
        fetchAuthor();
    }, {});

    let button = "";
    if (userId === authorId) {
        button = <Button variant="contained" href={`/profile/${userId}/manage`} userId={userId}>Manage Profile</Button>;
    }
   
    return (
        <div>
            <TopBar />
            <Typography variant="h3">{author.displayName}</Typography>
            <img alt="Profile" src={author.profileImage} style={{width:"40%"}}/>
            <Typography>Github URL: {author.github}</Typography>
            {button}
        </div>
    );
}