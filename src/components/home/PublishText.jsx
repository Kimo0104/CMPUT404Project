import React, { useState } from "react";
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import MenuItem from '@mui/material/MenuItem';
import { createPost, sendFriendInbox, sendPublicInbox } from "../../APIRequests.js";
import { userIdContext } from '../../App';

const formats = [
    {
        value: 'text/plain',
        label: 'Plain Text',
    },
    {
        value: 'text/markdown',
        label: 'Markdown',
    }
];
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

export default function PublishText(props) {
    const [format, setFormat] = useState("text/plain");
    const [visibility, setVisibility] = useState("PUBLIC");
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [content, setContent] = useState("");

    const { userId } = React.useContext(userIdContext);

    const handleFormatChange = (event) => {
        setFormat(event.target.value);
    };
    const handleVisibilityChange = (event) => {
        setVisibility(event.target.value);
    };
    const handleTitleChange = (event) => {
        setTitle(event.target.value);
    };
    const handleDescriptionChange = (event) => {
        setDescription(event.target.value);
    };
    const handleContentChange = (event) => {
        setContent(event.target.value);
    };

    const handlePublish = () => {
        props.handleCancel();
        const data = {
            type: "post",
            title: title,
            description: description,
            contentType: format,
            content: content,
            visibility: visibility,
            originalAuthor: userId
        }
        async function sendPostToInbox(){
            await createPost(userId, data)
                .then((response) => {
                    const postId = response.data.id
                    props.updateMyPosts(props.page, props.size);
                    if (visibility === "PUBLIC") sendPublicInbox(userId, postId)
                    if (visibility === "FRIENDS") sendFriendInbox(userId, postId)
                })
                .catch((reason) => {
                    props.handleError();
                });
        }
        sendPostToInbox();
    }
    return (
        <div>
            <DialogContent>
                <Grid container spacing={2}>
                <Grid item xs={12}>
                </Grid>
                <Grid 
                    style={{
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center"
                    }} 
                    item xs={6}>
                    <TextField
                    id="outlined-select-format"
                    select
                    label="Select"
                    value={format}
                    onChange={handleFormatChange}
                    helperText="Please select your text format">
                    {formats.map((option) => (
                        <MenuItem key={option.value} value={option.value}>
                        {option.label}
                        </MenuItem>
                    ))}
                    </TextField>
                </Grid>
                <Grid 
                    style={{
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center"
                    }} 
                    item xs={6}>
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
                    <TextField
                    autoFocus
                    margin="dense"
                    id="name"
                    label="Title"
                    fullWidth
                    onChange={handleTitleChange}
                    variant="standard"
                    />
                </Grid>
                <Grid item xs={12}>
                    <TextField
                    autoFocus
                    margin="dense"
                    id="name"
                    label="Description"
                    onChange={handleDescriptionChange}
                    fullWidth
                    variant="standard"
                    />
                </Grid>
                <Grid item xs={12}>
                    <TextField
                    autoFocus
                    margin="dense"
                    id="name"
                    label="Content"
                    fullWidth
                    onChange={handleContentChange}
                    variant="standard"
                    multiline
                    rows={5}
                    />
                </Grid>
                </Grid>
            </DialogContent>
            <DialogActions>
                <Button onClick={props.handleCancel}>Cancel</Button>
                <Button onClick={handlePublish}>Publish</Button>
            </DialogActions>
        </div>
    )
}
