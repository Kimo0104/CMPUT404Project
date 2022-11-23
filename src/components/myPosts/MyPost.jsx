import React, { useState } from "react";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { deletePost, modifyPost } from "../../APIRequests.js";
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

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
export default function BasicCard(props) {
  const [editOpen, setEditOpen] = useState(false);
  const [format, setFormat] = useState(props.item.contentType);
  const [title, setTitle] = useState(props.item.title);
  const [description, setDescription] = useState(props.item.description);
  const [content, setContent] = useState(props.item.content);

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
  const handleClickEditOpen = () => {
    setEditOpen(true);
  };
  const handleEditCancel = () => {
    setEditOpen(false);
  };
 

  const [deleteOpen, setDeleteOpen] = React.useState(false);

  const handleClickDeleteOpen = () => {
    setDeleteOpen(true);
  };

  const handleCancelDelete = () => {
    setDeleteOpen(false);
  };

  const handleDelete = () => {
    async function callDeletePost(){
      await deletePost(props.item.author, props.item.id)
    }
    callDeletePost();
    setDeleteOpen(false);
  };


  const handleEdit = () => {
    setEditOpen(false);
    const data = {
      title: title,
      description: description,
      contentType: format,
      content: content,
    }
    async function callModifyPost(){
      await modifyPost(props.item.author, props.item.id, data)
    }
    callModifyPost();
  }

  //props contains title, content
  return (
    <Card sx={{ minWidth: 275 }}  style={{backgroundColor: "#F9F0C1"}}>
      <Grid>
        <Grid container spacing={1}>
          <Grid item xs={10.8}>
          </Grid>
          <Grid item xs>
          <EditIcon variant="outlined" onClick={handleClickEditOpen}/>
          <DeleteIcon variant="outlined" onClick={handleClickDeleteOpen}/>
            <Dialog open={editOpen}>
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
                <Button onClick={handleEditCancel}>Cancel</Button>
                <Button onClick={handleEdit}>Publish</Button>
              </DialogActions>
            </Dialog>
            <Dialog
              open={deleteOpen}
              onClose={handleCancelDelete}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">
                {"Delete Post?"}
              </DialogTitle>
              <DialogContent>
                <DialogContentText id="alert-dialog-description">
                  This action cannot be undone.
                </DialogContentText>
              </DialogContent>
              <DialogActions>
                <Button onClick={handleCancelDelete}>Cancel</Button>
                <Button onClick={handleDelete}>
                  Delete
                </Button>
              </DialogActions>
            </Dialog>
          </Grid>
        </Grid>
      </Grid>
      <CardContent>
        <Typography sx={{ fontSize: 32 }} color="text.primary" gutterBottom>
          {props.item.title}
        </Typography>
        { props.item.contentType === "text/plain" &&
          <Typography sx={{ mb: 1.5, frontSize: 24 }} color="text.secondary">
            {content}
          </Typography>
        }
        { props.item.contentType === "text/markdown" &&
          <ReactMarkdown children={content} remarkPlugins={[remarkGfm]}/>
        }
      </CardContent>
    </Card>
  );
}