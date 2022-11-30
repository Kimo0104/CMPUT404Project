import { Avatar, Card, CardActionArea, Grid, Typography } from '@mui/material';
import * as React from 'react';
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthorIdContext, ShowSearchContext } from '../home/Home';

export default function ListItem ({author}) {

    
    const { setAuthorId } = React.useContext(AuthorIdContext);
    const { setShowSearch } = React.useContext(ShowSearchContext);

    const navigate = useNavigate();

    const handleClick = () => {
        //navigate(`/profile/${authorId}`, {authorId: authorId});
        setAuthorId(author.id);
        localStorage.setItem("authorId", author.id);
        setShowSearch("false");
        localStorage.setItem("showSearch", "false");
    }

    return (
        <div style={{justifyContent:"center", display: "flex", width:"100%"}}>
            <Card sx={{display:"block", width:"100%"}}>
                <CardActionArea onClick={handleClick} style={{width:"100%"}}>
                    <div style={{justifyContent:"center", display: "flex", paddingTop:"10px"}}>
                        <Avatar style={{width:"4em", height:"4em"}} src={author.profileImage} alt="Profile"/>
                    </div>
                    <Typography style={{fontSize:"2.5em", paddingLeft:"0.5em", paddingRight:"0.5em"}}>{author.displayName}</Typography>
                </CardActionArea>
            </Card>
        </div>
    );

}