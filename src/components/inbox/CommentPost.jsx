import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

import { getPost, getAuthor } from '../../APIRequests';
import CommentLike from '../like/CommentLike'

export default function BasicCard(props) {
  //props has commenterAuthorId, commentPostId, commentId, comment, contentType
  //likes show the title of the post with a desc "User liked this post!"
  const [commenterAuthor, setCommenterAuthor] = React.useState({});
  const [commentPost, setCommentPost] = React.useState({});

  React.useEffect(() => {
    async function loadInfo() {
      const commenterAuthor = await getAuthor(props.commenterAuthorId);
      setCommenterAuthor(commenterAuthor);
      const commentPost = await getPost(1, props.commentPostId);
      setCommentPost(commentPost);
    }
    loadInfo();
  }, [props]);

  return (
    <Card sx={{ minWidth: 275 }} style={{backgroundColor: "#FAF9F6"}}>
      <CardContent>
        <Typography sx={{ fontSize: 18 }} color="text.primary" gutterBottom>
          {commenterAuthor.displayName} commented on "{commentPost.title}":
        </Typography>
        { props.contentType === "text/plain" &&
          <Typography sx={{ mb: 1.5, frontSize: 16 }} color="text.secondary">
            {props.comment}
          </Typography>
        }
        { props.contentType === "text/markdown" &&
          <ReactMarkdown children={props.comment} remarkPlugins={[remarkGfm]} />
        }
      </CardContent>
      <Grid>
        <Grid container spacing={0.5}>
          <Grid item xs = {12}>
            <Typography sx={{ fontSize: 20, fontWeight: 'bold', marginLeft: 3 }} color="text.primary" align='left'>
            {commenterAuthor.displayName} commented on "{commentPost.title}":
            </Typography>
          </Grid>
          <Grid item xs = {12}sx={{ frontSize: 16, fontWeight: 'bold', marginLeft: 3.5 }}>
            { props.contentType === "text/plain" &&
              <Typography sx={{ frontSize: 16, fontWeight: 'bold'}} color="text.secondary" align='left'>
                {props.comment}
              </Typography>
            }
            { props.contentType === "text/markdown" &&
              <ReactMarkdown children={props.comment} remarkPlugins={[remarkGfm]}/>
            }
          </Grid>
          <Grid item xs align="center">
            <CommentLike authorId={props.commenterAuthorId} commentId={props.commentId} showCount={false}/>
          </Grid>
        </Grid>
      </Grid>
    </Card>
  );
}