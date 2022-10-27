import React, { useState } from "react";
import Grid from '@mui/material/Grid';
import TopBar from '../topbar/TopBar.jsx'
import PublishIcon from '@mui/icons-material/Publish';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import MenuItem from '@mui/material/MenuItem';
import Inbox from '../inbox/Inbox'
import { createPost, sendFriendInbox, sendPublicInbox } from "../../APIRequests.js";


const formats = [
  {
    value: 'text',
    label: 'Plain Text',
  },
  {
    value: 'markdown',
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
export default function Home() {
  const [open, setOpen] = useState(false);
  const [format, setFormat] = useState("text");
  const [visibility, setVisibility] = useState("PUBLIC");
  const [title, setTitle] = useState("");
  const [source, setSource] = useState("");
  const [origin, setOrigin] = useState("");
  const [description, setDescription] = useState("");
  const [content, setContent] = useState("");

  const handleFormatChange = (event) => {
    setFormat(event.target.value);
  };
  const handleVisibilityChange = (event) => {
    setVisibility(event.target.value);
  };
  const handleTitleChange = (event) => {
    setTitle(event.target.value);
  };
  const handleSourceChange = (event) => {
    setSource(event.target.value);
  };
  const handleOriginChange = (event) => {
    setOrigin(event.target.value);
  };
  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };
  const handleContentChange = (event) => {
    setContent(event.target.value);
  };
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleCancel = () => {
    setOpen(false);
  };

  const handlePublish = () => {
    setOpen(false);
    // Api calls here
    const authorId = 1;
    console.log(visibility)
    const data = {
      type: "post",
      title: title,
      source: source,
      origin: origin,
      description: description,
      contentType: format,
      content: content,
      visibility: visibility,
      originalAuthor: authorId
    }
    async function sendPostToInbox(){
      const response = await createPost(authorId, data);
      const postId = response.id
      if (visibility === "PUBLIC") sendPublicInbox(authorId, postId)
      if (visibility === "FRIENDS") sendFriendInbox(authorId, postId)
    }
    sendPostToInbox();
  }

  return (
    <div>
      <TopBar/>
        <div>
          <Grid container spacing={2}>
            <Grid item xs={2}>
            </Grid>
            <Grid item xs={8}>
                <Inbox authorId={1}/>
            </Grid>
            <Grid item xs={2}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
              </Grid>
              <Grid item xs={12}>
                <Button size="large" variant="outlined" onClick={handleClickOpen} endIcon={<PublishIcon />}>
                  Publish Post
                </Button>
                <Dialog open={open}>
                      <DialogTitle>Publish Post</DialogTitle>
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
                          <Grid item xs={6}>
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
                              label="Source"
                              onChange={handleSourceChange}
                              fullWidth
                              variant="standard"
                              />
                          </Grid>
                          <Grid item xs={12}>
                            <TextField
                              autoFocus
                              margin="dense"
                              id="name"
                              label="Origin"
                              onChange={handleOriginChange}
                              fullWidth
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
                        <Button onClick={handleCancel}>Cancel</Button>
                        <Button onClick={handlePublish}>Publish</Button>
                      </DialogActions>
                    </Dialog>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </div>
    </div>
  )
}
