import React, { useState } from "react";
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
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
                <Button size='large' startIcon={<AttachFileIcon/>} onClick={props.handleCancel}>Upload Image via File</Button>
                <Button size='large' startIcon={<LinkIcon/>} onClick={props.handleCancel}>Upload Image via URL</Button>
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
