import * as React from 'react';
import TopBar from '../topbar/TopBar.jsx';
import { getAuthor } from '../../APIRequests';
import { borderLeft } from '@mui/system';
import { Button, Typography } from '@mui/material';
import { useLocation } from 'react-router-dom';
import FriendRequestList from "../friendRequestList/FriendRequestList";
import Follow from "../follow/Follow";
import { userIdContext } from '../../App';
import { AuthorIdContext } from '../home/Home.jsx';

export default function Profile(props)  {

    const location = useLocation();
    
    const userId = React.useContext(userIdContext);

    const { authorId } = React.useContext(AuthorIdContext);
    const [author, setAuthor] = React.useState({});

    const fetchAuthor = async () => {
        const author = await getAuthor(authorId);
        setAuthor(author);
    };

    React.useEffect(() => {
        fetchAuthor();
    }, [authorId]);

    let button = "";
    let requestList = "";
    let followButton = "";
    if (userId === authorId) {
        button = <Button variant="contained" href={`/profile/${userId}/manage`} userId={userId}>Manage Profile</Button>;
        requestList = <FriendRequestList authorId={userId} />
    } else {
        followButton = <Follow authorId={userId} foreignAuthorId={authorId} />
    }
   
    return (
        <div>
            {/*<TopBar />*/}
            <Typography variant="h3">{author.displayName}</Typography>
            <img alt="Profile" src={author.profileImage} style={{width:"40%"}}/>
            <Typography>Github URL: {author.github}</Typography>
            {button}
            {requestList}
            {followButton}
        </div>
    );
}