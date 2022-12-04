import React, { useState } from "react";
import Grid from '@mui/material/Grid';
import PublishIcon from '@mui/icons-material/Publish';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import PublishTab from "./PublishTab.jsx"
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
export default function PublishButton(props) {
    const [error, setError] = useState(false);
    const handleError = () => {
        setError(true);
    };
    const handleCloseError = () => {
        setError(false);
    };

    const [open, setOpen] = useState(false);
    const handleClickOpen = () => {
        setOpen(true);
      };
    const handleCancel = () => {
        setOpen(false);
    };
    
    return (
        <Grid item xs={12}>
            <Button size="large" variant="contained" onClick={handleClickOpen} endIcon={<PublishIcon />}>
                Publish Post
            </Button>
            <Dialog open={open}>
                <DialogTitle>Publish Post</DialogTitle>
                <PublishTab 
                    handleClickOpen={handleClickOpen} 
                    handleCancel={handleCancel}
                    handleError = {handleError}
                    updateMyPosts={props.updateMyPosts} 
                    page={props.page} 
                    size={props.size}
                     />
            </Dialog>
            { error && <Snackbar open={error} autoHideDuration={3000} onClose={handleCloseError}>
                    <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
                        Error Creating the Post!
                    </Alert>
                </Snackbar>}
        </Grid>
    )
}
