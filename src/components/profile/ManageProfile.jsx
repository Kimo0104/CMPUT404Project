import * as React from 'react';
import TopBar from '../topbar/TopBar.jsx'
import { getAuthor, modifyAuthor } from '../../APIRequests'
import { borderLeft } from '@mui/system';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Grid, TextField, Typography } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';


export default function Profile(props)  {

    let userId = props.userId;
    
    const [author, setAuthor] = React.useState({});
    const [githubValue, setGithubValue] = React.useState("");

    const navigate = useNavigate();

    const fetchAuthor = async () => {
        const author = await getAuthor(userId);
        setAuthor(author);
        setGithubValue(author.github);
    };

    React.useEffect(() => {
        fetchAuthor();
    }, {});

    const [open, setOpen] = React.useState(false);
    const [link, setLink] = React.useState(author.profileImage);
    const [linkText, setLinkText] = React.useState(author.profileImage);

    const handleChange = (e) => {
        setGithubValue(e.target.value);
    }

    const handleApplyButtonPress = async (e) => {
        await modifyAuthor(userId, githubValue, link);
        console.log(link);
        navigate(`/profile/${userId}`, {userId: userId});
    }

    const handleCancelButtonPress = async (e) => {
        navigate(`/profile/${userId}`, {userId: userId});
    }

    const handleImagePress = async (e) => {
        setOpen(true);
    }

    const onDoneClicked = async (e) => {
        setLink(linkText);
        let img = document.getElementById("profileImage");
        img.src = linkText;
        setOpen(false);
    }

    const onDeleteClicked = async (e) => {
        setLink("");
        let generic_profile_image_path = "https://t3.ftcdn.net/jpg/05/16/27/58/360_F_516275801_f3Fsp17x6HQK0xQgDQEELoTuERO4SsWV.jpg"
        let img = document.getElementById("profileImage");
        img.src = generic_profile_image_path;
        setOpen(false);
    }

    const onCancelClicked = async (e) => {
        setOpen(false);
    }

    const onLinkChange = async (e) => {
        setLinkText(e.target.value);
        console.log(e.target.value);
    }
   
    return (
        <div>
            <TopBar />
            <Typography variant="h3">{author.displayName}</Typography>
            <img id="profileImage" alt="Profile" src={author.profileImage} style={{width:"40%"}} onClick={handleImagePress} />
            <Grid container spacing={1} style={{justifyContent: "center", display: "flex"}}>
                <Grid item xs={2} style={{paddingTop:"20px"}}>
                    <Typography>Github URL: </Typography>
                </Grid>
                <Grid item xs={2}>
                    <TextField value={githubValue} onChange={handleChange}/>
                </Grid>
            </Grid>
            <Grid container spacing={1} style={{justifyContent: "center", display: "flex", paddingTop:"20px"}}>
                <Grid item xs={4}>
                    <Button variant="contained" onClick={handleApplyButtonPress} style={{marginRight:"5px"}}>Apply</Button>
                    <Button variant="contained" onClick={handleCancelButtonPress} style={{marginLeft:"5px"}}>Cancel</Button>
                </Grid>
            </Grid>
            <Dialog open={open}>
                <DialogTitle>Change Profile Image</DialogTitle>
                <DialogContent>
                    <TextField placeholder='Choose Link' onChange={onLinkChange}></TextField>
                </DialogContent>
                <DialogActions>
                    <Button onClick={onDeleteClicked}>Delete</Button>
                    <Button onClick={onCancelClicked}>Cancel</Button>
                    <Button onClick={onDoneClicked}>Done</Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}