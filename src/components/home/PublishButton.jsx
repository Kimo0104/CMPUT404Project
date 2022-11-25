import React, { useState } from "react";
import Grid from '@mui/material/Grid';
import PublishIcon from '@mui/icons-material/Publish';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import PublishTab from "./PublishTab.jsx"

export default function PublishButton(props) {
    const [open, setOpen] = useState(false);
    const handleClickOpen = () => {
        setOpen(true);
      };
    const handleCancel = () => {
        setOpen(false);
    };
    
    return (
        <Grid item xs={12}>
            <Button size="large" variant="outlined" onClick={handleClickOpen} endIcon={<PublishIcon />}>
                Publish Post
            </Button>
            <Dialog open={open}>
                <DialogTitle>Publish Post</DialogTitle>
                <PublishTab handleClickOpen={handleClickOpen} handleCancel={handleCancel}/>
            </Dialog>
        </Grid>
    )
}
