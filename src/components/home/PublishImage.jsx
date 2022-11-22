import React, { useState } from "react";
import Button from '@mui/material/Button';
import DialogActions from '@mui/material/DialogActions';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import LinkIcon from '@mui/icons-material/Link';
import AttachFileIcon from '@mui/icons-material/AttachFile';
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

    const handleVisibilityChange = (event) => {
        setVisibility(event.target.value);
    };
    const handlePublish = () => {
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
