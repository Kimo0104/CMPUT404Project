import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import FavoriteBorderTwoToneIcon from '@mui/icons-material/FavoriteBorderTwoTone';
import ShareOutlinedIcon from '@mui/icons-material/ShareOutlined';
import IconButton from '@mui/material/IconButton';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';

import { getAuthor } from '../../APIRequests'

export default function BasicCard(props) {
  //props contains title, content, authorId
  //textPosts have a title, a description, a share button, a comments button, and a like button
  const [author, setAuthor] = React.useState({});

  React.useEffect(() => {
    async function loadAuthor() {
      const author = await getAuthor(props.authorId);
      setAuthor(author);
    }
    loadAuthor();
  }, [props]);

  return (
    <Card sx={{ minWidth: 275 }}>
      <Typography sx={{ fontSize: 16, marginRight: 1}} color="text.secondary" align='right'>
        {author.displayName}
      </Typography>
      <CardContent>
        <Typography sx={{ fontSize: 32 }} color="text.primary" gutterBottom>
          {props.title}
        </Typography>
        <Typography sx={{ mb: 1.5, frontSize: 24 }} color="text.secondary">
          {props.content}
        </Typography>
      </CardContent>
      <Grid>
        <Grid container spacing={2}>
          <Grid item xs>
            <IconButton aria-label="like">
              <FavoriteBorderTwoToneIcon />
            </IconButton>
          </Grid>
          <Grid item xs>
            <IconButton aria-label="share">
              <ShareOutlinedIcon />
            </IconButton>
          </Grid>
          <Grid item xs>
            <IconButton aria-label="comments">
              <ChatBubbleOutlineIcon />
            </IconButton>
          </Grid>
        </Grid>
      </Grid>
    </Card>
  );
}