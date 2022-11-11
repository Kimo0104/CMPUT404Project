import * as React from 'react';
import TopBar from '../topbar/TopBar.jsx'
import { getAuthor, modifyAuthor, uploadImage } from '../../APIRequests'
import { borderLeft } from '@mui/system';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Grid, TextField, Typography } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import { userIdContext } from '../../App.js';
import { SERVER_URL } from '../../APIRequests';


export default function ManageProfile(props)  {

    const userId = React.useContext(userIdContext);
    
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
    }, []);

    const [open, setOpen] = React.useState(false);
    const [link, setLink] = React.useState("");
    const [linkText, setLinkText] = React.useState("");
    const [imageFile, setImageFile] = React.useState(Object);
    const [imageUploaded, setImageUploaded] = React.useState(false);

    const handleChange = (e) => {
        setGithubValue(e.target.value);
    }

    const handleApplyButtonPress = async (e) => {
        if (imageUploaded) {
            uploadImage(userId, imageFile);
        }
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

    const onDialogDoneClicked = async (e) => {
        setImageUploaded(false);
        // If an image was uploaded, display that image, else display the 
        // current profile image or whatever the user set the link of the 
        // profile image to.
        if (!imageUploaded) {
            // If empty link, use user's current profile image, else
            // set the link of the profile image to what the user specified
            console.log("onDoneClicked", linkText)
            if (typeof linkText === "undefined" || linkText.trim() === "") {
                setLink(setImageSource(author.profileImage));
            } else {
                setLink(setImageSource(linkText));
            }
        }
        setOpen(false);
    }

    const onDialogDeleteClicked = async (e) => {
        let generic_profile_image_path = "https://t3.ftcdn.net/jpg/05/16/27/58/360_F_516275801_f3Fsp17x6HQK0xQgDQEELoTuERO4SsWV.jpg"
        setImageSource(generic_profile_image_path);
        setLink(generic_profile_image_path);
        setImageUploaded(false);
        setOpen(false);
    }

    const onDialogCancelClicked = async (e) => {
        setOpen(false);
    }

    const onLinkChange = async (e) => {
        setLinkText(e.target.value);
        setImageUploaded(false);
    }

    //https://stackoverflow.com/a/46120369
    const onImageUpload = async (e) => {
        let file = e.target.files[0];
        
        if (file) {
            //let contents = await file.text(); 
            setImageFile(file);
            setImageUploaded(true);
            setLink(SERVER_URL+`/images/${userId}`)
            setImageSource(URL.createObjectURL(file));
            setOpen(false);
        }
    }

    const setImageSource = (URL) => {
        let img = document.getElementById("profileImage");
        img.src = URL;
        console.log(img.src);
        return img.src;
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
                    <TextField placeholder='Choose Link' onChange={onLinkChange} onPaste={onLinkChange}></TextField>
                    {/* https://stackoverflow.com/a/49408555 */}
                    <input accept="image/*" style={{ display: 'none' }} id="raised-button-file" type="file" onChange={onImageUpload}/>
                    <label htmlFor="raised-button-file">
                        <Button variant="raised" component="span">
                            Upload
                        </Button>
                    </label> 
                </DialogContent>
                <DialogActions>
                    <Button onClick={onDialogDeleteClicked}>Delete</Button>
                    <Button onClick={onDialogCancelClicked}>Cancel</Button>
                    <Button onClick={onDialogDoneClicked}>Done</Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}