/* eslint-disable */
import React, { useState } from "react";
import Card from '@mui/material/Card';
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
import { deletePost } from "../../APIRequests.js";
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import ModifyPost from './ModifyPost.jsx'

export default function BasicCard(props) {
  const [editOpen, setEditOpen] = useState(false);
  const handleClickEditOpen = () => {
    setEditOpen(true);
  };
  const handleEditCancel = () => {
    setEditOpen(false);
  };
 
  const [deleteOpen, setDeleteOpen] = useState(false);

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

  //props contains title, content
  return (
    <Card sx={{ minWidth: 275 }}  style={{backgroundColor: "#FAF9F6"}}>
      <Grid>
        <Grid container spacing={0.5}>
          <Grid item xs={10.8}>
            </Grid>
              <Grid item xs={8} sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'flex-start' }}>
                <Typography sx={{ fontSize: 26, fontWeight: 'bold', marginLeft: 3 }} color="text.primary" align='left'>
                  {props.item.title}
                </Typography>
              </Grid>
            <Grid item xs={3.7} sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'flex-end' }}>
              <EditIcon variant="outlined" onClick={handleClickEditOpen}/>
              <DeleteIcon variant="outlined" onClick={handleClickDeleteOpen}/>
              <ModifyPost 
                handleEditCancel={handleEditCancel}
                editOpen={editOpen}
                author={props.item.author}
                id = {props.item.id}
                contentType = {props.item.contentType}
                content = {props.item.content}
                description = {props.item.description}
                title = {props.item.title}
                />
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
          <Grid item xs={12} sx={{ marginLeft: 3.5 }}>
            { props.item.contentType === "text/plain" &&
              <Typography sx={{ mb: 0, frontSize: 24, alignItems: 'flex-start'}} color="text.secondary" align='left'>
                {props.item.content}
              </Typography>
            }
            { props.item.contentType === "text/markdown" &&
              <ReactMarkdown children={props.item.content} remarkPlugins={[remarkGfm]}/>
            }
            { props.item.contentType === "image" &&
              <img src={props.item.content}/>
            }
          </Grid>
          <Grid item xs = {12}/>
        </Grid>
      </Grid>
    </Card>
  );
}