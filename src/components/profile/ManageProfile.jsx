import * as React from 'react';
import TopBar from '../topbar/TopBar.jsx'
import { getAuthor, modifyAuthor, uploadImage } from '../../APIRequests'
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Grid, TextField, Tooltip, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { userIdContext } from '../../App.js';
import { SERVER_URL } from '../../APIRequests';


export default function ManageProfile(props)  {

    // Get the ID of the user
    const { userId } = React.useContext(userIdContext);
    
    // Get the author object corresponding to the user
    const [author, setAuthor] = React.useState({});
    const [githubValue, setGithubValue] = React.useState("");
    const [imageLink, setImageLink] = React.useState("");

    const navigate = useNavigate();

    const fetchAuthor = async () => {
        const author = await getAuthor(userId);
        setAuthor(author);
        setGithubValue(author.github);
        setImageLink(author.profileImage);
    };

    React.useEffect(() => {
        fetchAuthor();
    }, []);

    const [open, setOpen] = React.useState(false);
    const [imageLinkText, setImageLinkText] = React.useState("");
    const [imageFile, setImageFile] = React.useState(Object);
    const [imageUploaded, setImageUploaded] = React.useState(false);

    const handleGithubChange = (e) => {
        setGithubValue(e.target.value);
    }

    const handleApplyButtonPress = async (e) => {
        //if (imageUploaded) {
        //    uploadImage(userId, imageFile);
        //}
        modifyAuthor(userId, githubValue, imageLink).then();
        navigate("/home");
    }

    const handleCancelButtonPress = async (e) => {
        navigate("/home");
        let token = localStorage.getItem("token");
        localStorage.clear();
        localStorage.setItem("userId", userId);
        localStorage.setItem("token", token);
    }

    const handleImagePress = async (e) => {
        setOpen(true);
    }

    const onDialogDoneClicked = async (e) => {
        // Done will only be clicked if the user enters a link. If they upload an image
        // the dialog box just closes.

        // If empty link, use user's current profile image, else
        // set the link of the profile image to what the user specified
        if (typeof imageLinkText === "undefined" || imageLinkText.trim() === "") {
            setImageLink(setImageSource(author.profileImage));
        } else {
            setImageLink(setImageSource(imageLinkText));
        }
        setOpen(false);
    }

    // If an image is to be deleted, it sets the profileImage to a generic image
    const onDialogDeleteClicked = async (e) => {
        // This image is licensed under Adobe Standard License
        let generic_profile_image_path = "https://t3.ftcdn.net/jpg/05/16/27/58/360_F_516275801_f3Fsp17x6HQK0xQgDQEELoTuERO4SsWV.jpg"
        setImageSource(generic_profile_image_path);
        setImageLink(generic_profile_image_path);
        setImageUploaded(false);
        setOpen(false);
    }

    const onDialogCancelClicked = async (e) => {
        setOpen(false);
    }

    // Handles changing an image link
    const onImageLinkChange = async (e) => {
        setImageLinkText(e.target.value);
        setImageUploaded(false);
    }

    // Handles uploadiing an image file - https://stackoverflow.com/a/46120369
    const onImageUpload = async (e) => {
        let file = e.target.files[0];
        
        if (file) {
            // Checks if the file is an image or not
            if (file["type"].includes("image/")) {
                setImageFile(file);
                setImageUploaded(true);

                const reader = new FileReader();
                reader.onload = async (e) => {
                    // https://stackoverflow.com/a/52311051
                    setImageLink(e.target.result)
                };
                // https://stackoverflow.com/questions/10982712/convert-binary-data-to-base64-with-javascript
                reader.readAsDataURL(file);

                setImageSource(URL.createObjectURL(file));
            } else {
                alert("Invalid file type! Please upload an image.");
            }
            setOpen(false);
        }
    }

    const setImageSource = (URL) => {
        // Sets the source of profile image
        let img = document.getElementById("profileImage");
        img.src = URL;
        return img.src;
    }
   
    return (
        <div>
            <TopBar />
            <Typography variant="h3">{author.displayName}</Typography>
            <Tooltip title="Change Profile Image" followCursor>
                <img id="profileImage" alt="Profile" src={imageLink} style={{width:"40%"}} onClick={handleImagePress} />
            </Tooltip>
            <Grid container spacing={1} style={{justifyContent: "center", display: "flex"}}>
                <Grid item xs={2} style={{paddingTop:"20px"}}>
                    <Typography>Github URL/Username: </Typography>
                </Grid>
                <Grid item xs={2}>
                    <TextField value={githubValue} onChange={handleGithubChange}/>
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
                    <TextField placeholder='Choose Link' onChange={onImageLinkChange} onPaste={onImageLinkChange}></TextField>
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