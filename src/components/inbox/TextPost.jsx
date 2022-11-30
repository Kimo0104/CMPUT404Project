/* eslint-disable */
import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';

import Share from '../share/Share'
import Comment from '../comment/Comment'
import Like from '../like/Like'
import { getAuthor } from '../../APIRequests'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function BasicCard(props) {
  //props contains authorId, postId, title, source, origin, description, content, contentType, originalAuthor, visibility
  //textPosts have a title, a description, a share button, a comments button, and a like button
  const [postAuthor, setPostAuthor] = React.useState(false);

  React.useEffect(() => {
    async function loadInfo() {
      const postAuthor = await getAuthor(props.originalAuthor);
      setPostAuthor(postAuthor);
    }
    loadInfo();
  }, [props]);

  if (!postAuthor) {
    return;
  }

  return (
    <Card sx={{ minWidth: 275 }}  style={{backgroundColor: "#FAF9F6"}}>
      <Grid>
        <Grid container spacing={0.5}>
          <Grid item xs={8} sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'flex-start' }}>
            <Typography sx={{ fontSize: 26, fontWeight: 'bold', marginLeft: 3 }} color="text.primary" align='left'>
              {props.title}
            </Typography>
          </Grid>
          <Grid item xs={4} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
            <Typography sx={{ fontSize: 16, fontWeight: 'bold', marginRight: 1 }} color="text.secondary" align='right'>
              Post by {postAuthor.displayName}
            </Typography>
          </Grid>
          <Grid item xs={12} sx={
              { 
                display: 'flex', 
                alignItems: 'flex-start', 
                justifyContent: props.contentType === "image" ? 'center' : 'flex-start', 
                marginLeft: 3.5 
              }}
          >
            { props.contentType === "text/plain" &&
              <Typography sx={{ mb: 1.5, frontSize: 24 }} color="text.secondary">
                {props.content}
              </Typography>
            }
            { props.contentType === "text/markdown" &&
              <ReactMarkdown children={props.content} remarkPlugins={[remarkGfm]} />
            }
            { props.contentType === "image" &&
              <img src={props.content}/>
            }
          </Grid>
          <Grid item xs align="center">
            <Like authorId={props.authorId} postId={props.postId} showCount={props.visibility === "FRIEND"}/>
          </Grid>
          <Grid item xs align="center" >
            <Share 
              authorId={props.authorId}
              postId={props.postId}
              title={props.title}
              source={props.source}
              origin={props.origin}
              description={props.description}
              contentType={props.contentType}
              content={props.content}
              originalAuthor={props.originalAuthor}
              visiblity={props.visibility}
            />
          </Grid>
          <Grid item xs align="center">
            <Comment 
              authorId={props.authorId}
              postId={props.postId}
              posterId={postAuthor.id}
            />
          </Grid>
        </Grid>
      </Grid>
    </Card>
  );
}