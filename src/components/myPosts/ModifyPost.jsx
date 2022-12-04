import React, { useState } from "react";
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import { modifyPost } from "../../APIRequests.js";
import DialogTitle from '@mui/material/DialogTitle';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import LinkIcon from '@mui/icons-material/Link';
import AttachFileIcon from '@mui/icons-material/AttachFile';

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

export default function ModifyPost(props) {
    const [format, setFormat] = useState(props.contentType);
    const [title, setTitle] = useState(props.title);
    const [description, setDescription] = useState(props.description);
    const [content, setContent] = useState(props.content);

    const handleFormatChange = (event) => {
        setFormat(event.target.value);
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
    const handleEdit = () => {
        props.handleEditCancel();
        if (props.contentType != 'image'){
            const data = {
                title: title,
                description: description,
                contentType: format,
                content: content,
            }
            async function callModifyPost(){
                await modifyPost(props.author, props.id, data)
            }
            callModifyPost();
        }
        else if (imageURL != "") {
            const data = {content: imageURL}
            async function callModifyPost(){
                await modifyPost(props.author, props.id, data)
            }
            callModifyPost();
        }
        else{
            const reader = new FileReader();
            reader.onload = async (e) => {
                const image = e.currentTarget.result;
                const data = {content: image}
                async function callModifyPost(){
                    await modifyPost(props.author, props.id, data)
                }
                callModifyPost();
            };
            reader.readAsDataURL(selectedImage);
        }
        props.updateMyPosts(props.page, props.size);
    }
    const [selectedImage, setSelectedImage] = useState(null);
    const [urlTextBox, setUrlTextBox] = useState(false);
    const [imageURL, setImageURL] = useState("");
    if (props.contentType != 'image') return (
        <Dialog open={props.editOpen}>
            <DialogTitle>Edit Post</DialogTitle>
            <DialogContent>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                </Grid>
                <Grid item xs={6}>
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
                <Grid item xs={12}>
                <TextField
                    autoFocus
                    margin="dense"
                    id="name"
                    value={title}
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
                    value={description}
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
                    value={content}
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
            <Button onClick={props.handleEditCancel}>Cancel</Button>
            <Button onClick={handleEdit}>Publish</Button>
            </DialogActions>
        </Dialog>
    )
    if (props.contentType == 'image') return (
        <Dialog open={props.editOpen}>
            <Grid container spacing={2}>
                <Grid item xs={12}>
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
                            <Button onClick={props.handleEditCancel}>Cancel</Button>
                            <Button onClick={handleEdit}>Publish</Button>
                    </DialogActions>
                </Grid>
            </Grid>
        </Dialog>
    )   
}
