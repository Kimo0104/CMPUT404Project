import { Avatar, Card, CardActionArea, Typography } from '@mui/material';
import * as React from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function ListItem ({author}) {

    let displayName = author.displayName;

    const navigate = useNavigate();

    const handleClick = () => {
        navigate(`/profile/${displayName}`, {userId: author.id})
    }

    return (
        <div style={{justifyContent:"center", display: "flex"}}>
            <Card>
                <CardActionArea onClick={handleClick} style={{width:"40vw"}}>
                    <div style={{justifyContent:"center", display: "flex", paddingTop:"10px"}}>
                        <Avatar style={{width:`${0.4*40}vw`, height:`${0.4*40}vw`}} src={author.profileImage} alt="Profile"/>
                    </div>
                    <Typography style={{fontSize:"2.5em"}}>{displayName}</Typography>
                </CardActionArea>
            </Card>
        </div>
    );

}