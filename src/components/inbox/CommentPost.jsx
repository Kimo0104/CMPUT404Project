import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

import { getPost, getAuthor } from '../../APIRequests';

export default function BasicCard(props) {
  //props has commenterAuthorId, commentPostId, comment
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
    <Card sx={{ minWidth: 275 }}>
      <CardContent style={{backgroundColor: "#F8B195"}}>
        <Typography sx={{ fontSize: 18 }} color="text.primary" gutterBottom>
          {commenterAuthor.displayName} commented on "{commentPost.title}":
        </Typography>
        <Typography sx={{ mb: 1.5, frontSize: 14 }} color="text.secondary">
          {props.comment}
        </Typography>
      </CardContent>
    </Card>
  );
}