/* eslint-disable */
import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import IconButton from '@mui/material/IconButton';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';

import { createComment, checkFollowStatus } from '../../APIRequests';

const contentTypes = [
    {
      value: 'text/plain',
      label: 'Plain Text',
    },
    {
      value: 'text/markdown',
      label: 'Markdown',
    }
  ];
export default function FormDialog(props) {
  //props contains authorId, postId, posterId

  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const [isFriends, setIsFriends] = React.useState(false);
  
  React.useEffect(() => {
    async function loadAuthor() {
        const following = await checkFollowStatus(props.authorId, props.posterId);
        const followed = await checkFollowStatus(props.posterId, props.authorId);
        console.log(props.authorId, props.posterId);
        setIsFriends(following === 2 && followed === 2);
    }
    loadAuthor();
  }, []);
  
  const [contentType, setContentType] = React.useState("text/plain");
  
  const handleFormatChange = (event) => {
    setContentType(event.target.value);
  };

  const [comment, setComment] = React.useState('');

  const handleCommentChange = (event) => {
    setComment(event.target.value);
  }

  const sendComment = () => {
    if (!open) { return; }

    const data = {
      comment: comment,
      contentType: "text/plain"
    }
    createComment(props.authorId, props.postId, data);
    setOpen(false);
  };

  if (!isFriends) {
    return;
  }

  return (
    <DialogContentText align="center">
      <IconButton onClick={handleClickOpen}>
        <ChatBubbleOutlineIcon />
      </IconButton>
      <Dialog open={open} onClose={handleClose} fullWidth={true} maxWidth={'sm'} align="center">
        <DialogTitle sx={{ fontSize: 32 }}>Comment on Post</DialogTitle>
        <DialogContent>
          <Grid container rowSpacing={4} paddingBottom={5} paddingTop={1}>
            <Grid item xs={12}>
                <TextField
                    id="outlined-select-format"
                    select
                    label="Select"
                    value={contentType}
                    onChange={handleFormatChange}
                    helperText="Please select your text format">
                    {contentTypes.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                        {option.label}
                    </MenuItem>
                    ))}
                </TextField>
            </Grid>
            <Grid style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center"
                }}
                item xs={12}>
                <TextField
                  id="outlined-multiline-static"
                  fullWidth
                  onChange={handleCommentChange}
                  multiline
                  rows={6}
                />
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
                  <Button onClick={sendComment} color="success" variant="contained">Comment</Button>
                </DialogContentText>
              </Grid>
          </Grid>
        </DialogContent>
      </Dialog>
    </DialogContentText>
  );
}
