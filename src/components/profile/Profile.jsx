import * as React from 'react';
import { getAuthor, getImage } from '../../APIRequests';
import { Button, Typography } from '@mui/material';
import Follow from "../follow/Follow";
import { userIdContext } from '../../App';
import { AuthorIdContext } from '../home/Home.jsx';

export default function Profile()  {
    
    const { userId }  = React.useContext(userIdContext);

    const { authorId } = React.useContext(AuthorIdContext);
    const [author, setAuthor] = React.useState({});

    const fetchAuthor = async () => {
        const author = await getAuthor(authorId);
        if (author.profileImage.trim() === "") {
            author.profileImage = "https://t3.ftcdn.net/jpg/05/16/27/58/360_F_516275801_f3Fsp17x6HQK0xQgDQEELoTuERO4SsWV.jpg";
        }
        setAuthor(author);
    };

    React.useEffect(() => {
        fetchAuthor();
    }, [authorId]);

    let button = "";
    let followButton = "";
    if (userId === authorId) {
        button = <Button variant="contained" href={`/profile/${userId}/manage`}>Manage Profile</Button>;
    } else {
        followButton = <Follow authorId={userId} foreignAuthorId={authorId} />
    }
   
    return (
        <div>
            <Typography variant="h3">{author.displayName}</Typography>
            <img alt="Profile" src={author.profileImage} style={{width:"40%"}}/>
            <Typography>Github URL/Username: {author.github}</Typography>
            {button}
            {followButton}
        </div>
    );
}