import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import IconButton from '@mui/material/IconButton';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';

import Share from '../share/Share'
import Like from '../like/Like'
import { getAuthor } from '../../APIRequests'
import ReactMarkdown from 'react-markdown'

export default function BasicCard(props) {
  //props contains authorId, postId, title, source, origin, description, content, contentType, originalAuthor
  //textPosts have a title, a description, a share button, a comments button, and a like button
  const [postAuthor, setPostAuthor] = React.useState({});

  React.useEffect(() => {
    async function loadInfo() {
      const postAuthor = await getAuthor(props.originalAuthor);
      setPostAuthor(postAuthor);
    }
    loadInfo();
  }, [props]);

  return (
    <Card sx={{ minWidth: 275 }}  style={{backgroundColor: "#F9F0C1"}}>
      <Typography sx={{ fontSize: 16, marginLeft: 1}} color="text.secondary" align='left'>
        From: {postAuthor.displayName}
      </Typography>
      <CardContent>
        <Typography sx={{ fontSize: 32 }} color="text.primary" gutterBottom>
          {props.title}
        </Typography>
        { props.contentType === "text/plain" &&
          <Typography sx={{ mb: 1.5, frontSize: 24 }} color="text.secondary">
            {props.content}
          </Typography>
        }
        { props.contentType === "text/markdown" &&
          <ReactMarkdown children={props.content} />
        }
      </CardContent>
      <Grid>
        <Grid container spacing={2}>
          <Grid item xs align="center">
            <Like authorId={props.authorId} postId={props.postId}/>
          </Grid>
          <Grid item xs align="center">
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
            />
          </Grid>
          <Grid item xs align="center">
            <IconButton aria-label="comments">
              <ChatBubbleOutlineIcon />
            </IconButton>
          </Grid>
        </Grid>
      </Grid>
    </Card>
  );
}