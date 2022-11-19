import * as React from 'react';
import TopBar from '../topbar/TopBar.jsx';
import { getAuthor } from '../../APIRequests';
import { Button, Typography } from '@mui/material';
import { useLocation } from 'react-router-dom';
import Follow from "../follow/Follow";
import { userIdContext } from '../../App';

export default function Profile(props)  {

    const location = useLocation();
    
    const userId = React.useContext(userIdContext);

    let authorId = location.pathname.split("/").at(-1);
    const [author, setAuthor] = React.useState({});

    const fetchAuthor = async () => {
        const author = await getAuthor(authorId);
        setAuthor(author);
    };

    React.useEffect(() => {
        fetchAuthor();
    }, []);

    let button = "";
    let followButton = "";
    if (userId === authorId) {
        button = <Button variant="contained" href={`/profile/${userId}/manage`} userId={userId}>Manage Profile</Button>;
    } else {
        followButton = <Follow authorId={userId} foreignAuthorId={authorId} />
    }
   
    return (
        <div>
            <TopBar />
            <Typography variant="h3">{author.displayName}</Typography>
            <img alt="Profile" src={author.profileImage} style={{width:"40%"}}/>
            <Typography>Github URL: {author.github}</Typography>
            {button}
            {followButton}
        </div>
    );
}