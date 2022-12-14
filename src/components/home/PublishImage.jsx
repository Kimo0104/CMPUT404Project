/* eslint-disable */
import React, { useState } from "react";
import Button from '@mui/material/Button';
import DialogActions from '@mui/material/DialogActions';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import LinkIcon from '@mui/icons-material/Link';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import { userIdContext } from '../../App';
import { createPost, sendFriendInbox, sendPublicInbox } from "../../APIRequests.js";

const visibilities = [
    {
        value: 'PUBLIC',
        label: 'Public',
    },
    {
        value: 'FRIENDS',
        label: 'Friends Only',
    },
    {
        value: 'UNLISTED',
        label: 'Unlisted',
    }
];
export default function PublishImage(props) {
    const [visibility, setVisibility] = useState("PUBLIC");
    const [selectedImage, setSelectedImage] = useState(null);
    const [urlTextBox, setUrlTextBox] = useState(false);
    const [imageURL, setImageURL] = useState("");

    const authorId = React.useContext(userIdContext).userId;

    const handleVisibilityChange = (event) => {
        setVisibility(event.target.value);
    };
    const handlePublish = () => {
        if (imageURL != "") handleUploadURL();
        if (selectedImage != null) handleUploadFile();
    }

    const handleUploadFile = () => {
        props.handleCancel();
        const reader = new FileReader();
        reader.onload = async (e) => {
            const image = e.currentTarget.result;
            const data = {
                contentType: 'image',
                content: image,
                visibility: visibility,
                originalAuthor: authorId
            }
            async function sendPostToInbox(){
                await createPost(authorId, data)
                    .then((response) => {
                        const postId = response.data.id
                        props.updateMyPosts(props.page, props.size);
                        if (visibility === "PUBLIC") sendPublicInbox(authorId, postId)
                        if (visibility === "FRIENDS") sendFriendInbox(authorId, postId)
                    })
                    .catch((reason) => {
                        props.handleError();
                    });
            }
            sendPostToInbox();
        };
        reader.readAsDataURL(selectedImage);
    }

    const handleUploadURL = () => {
        props.handleCancel();
        const data = {
            contentType: 'image',
            content: imageURL,
            visibility: visibility,
            originalAuthor: authorId
        }
        async function sendPostToInbox(){
            await createPost(authorId, data)
                .then((response) => {
                    const postId = response.data.id
                    if (visibility === "PUBLIC") sendPublicInbox(authorId, postId)
                    if (visibility === "FRIENDS") sendFriendInbox(authorId, postId)
                })
                .catch((reason) => {
                    props.handleError();
                });
        }
        sendPostToInbox();
    }

    return (
        <Grid container spacing={2}>
            <Grid item xs={12}>
            </Grid>
            <Grid style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center"
                }}
                item xs={12}>
                <TextField
                id="outlined-select-visibility"
                select
                label="Select"
                value={visibility}
                onChange={handleVisibilityChange}
                helperText="Please select your post visibility">
                {visibilities.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                    {option.label}
                    </MenuItem>
                ))}
                </TextField>
            </Grid>
            <Grid item xs={12}>
            </Grid>
            <Grid item xs={12}>
            </Grid>
            <Grid item xs={12}>
            </Grid>
            <Grid 
                container
                direction="column" 
                alignItems="center" 
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center"
                }}
                item xs={12}>
                {!urlTextBox && <Button size='large' component="label" startIcon={<AttachFileIcon/>}>
                    Upload Image via File
                    <input
                        type="file"
                        name="myImage"
                        hidden
                        onChange={(event) => {
                        setSelectedImage(event.target.files[0]);
                        }}
                    />
                </Button>}
                {selectedImage && <img alt="Uploaded Image" width={"250px"} src={URL.createObjectURL(selectedImage)} />}
                {selectedImage === null && <Button size='large' startIcon={<LinkIcon/>} onClick={() => setUrlTextBox(true)}>Upload Image via URL</Button>}
                {urlTextBox && <TextField
                    id="outlined-name"
                    label="Image URL"
                    value={imageURL}
                    onChange={(event) => setImageURL(event.target.value)}
                />}
            </Grid>
            <Grid item xs={12}>
                <DialogActions>
                        <Button onClick={props.handleCancel}>Cancel</Button>
                        <Button onClick={handlePublish}>Publish</Button>
                </DialogActions>
            </Grid>
        </Grid>
  )
}
