/* eslint-disable */
import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Grid from '@mui/material/Grid';
import IconButton from '@mui/material/IconButton';
import ShareOutlinedIcon from '@mui/icons-material/ShareOutlined';

import { createPost, sendFriendInbox, sendPublicInbox } from '../../APIRequests'

export default function FormDialog(props) {
  // props contains authorId, title, source, origin, description, format, content, originalAuthorId
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const sharePost = () => {
    if (!open) { return; }

    //creates post
    const data = {
      type: "post",
      title: props.title,
      source: props.source,
      origin: props.origin,
      description: props.description,
      contentType: props.format,
      content: props.content,
      visibility: "PUBLIC",
      originalAuthor: props.originalAuthorId
    }
    async function sendPostToInbox(){
      const response = await createPost(props.authorId, data);
      const postId = response.id
      //places post in necessary inbox
      if (data.visibility === "PUBLIC") { sendPublicInbox(props.authorId, postId) }
      if (data.visibility === "FRIENDS") { sendFriendInbox(props.authorId, postId) }
    }
    sendPostToInbox();

    setOpen(false);
  };

  return (
    <DialogContentText align="center">
      <IconButton onClick={handleClickOpen}>
        <ShareOutlinedIcon />
      </IconButton>
      <Dialog open={open} onClose={handleClose} fullWidth={true} maxWidth={'sm'} align="center">
        <DialogTitle sx={{ fontSize: 32 }}>Share Post</DialogTitle>
        <DialogContent>
          <Grid container rowSpacing={4} paddingBottom={10}>
              <Grid item xs = {12}>
                <DialogContentText align="center">
                    REPLACE THIS WITH PERSON GROUP SELECTION
                </DialogContentText>
              </Grid>
          </Grid>
          <Grid container>
              <Grid item xs={6}>
                <DialogContentText align="center">
                  <Button onClick={handleClose} color="error" variant="contained">Cancel</Button>
                </DialogContentText>
              </Grid>
              <Grid item xs={6}>
                <DialogContentText align="center">
                  <Button onClick={sharePost} color="success" variant="contained">Send</Button>
                </DialogContentText>
              </Grid>
          </Grid>
        </DialogContent>
      </Dialog>
    </DialogContentText>
  );
}
