/* eslint-disable */
import * as React from 'react';
import DialogContentText from '@mui/material/DialogContentText';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import FavoriteBorderTwoToneIcon from '@mui/icons-material/FavoriteBorderTwoTone';
import FavoriteTwoToneIcon from '@mui/icons-material/FavoriteTwoTone';
import IconButton from '@mui/material/IconButton';

import { getAuthorPostLiked, createPostLike, deletePostLike, getPostLikes } from '../../APIRequests'

export default function FormDialog(props) {
  //props has authorId, postId, showCount
  const [debounce, setDebounce] = React.useState((new Date()).getTime());
  const [liked, setLiked] = React.useState(false);
  const [count, setCount] = React.useState(0);

  React.useEffect(() => {
    async function loadInfo() {
      const liked = await getAuthorPostLiked(props.authorId, props.postId);
      setLiked(liked);
      if (props.showCount) {
        const likes = await getPostLikes(props.postId);
        setCount(likes.length);
      }
    }
    loadInfo();
  }, [props]);

  const handleSendLike = () => {
    const nowTimeMilli = (new Date()).getTime()
    if (nowTimeMilli < debounce + 500) { return; }
    setDebounce(nowTimeMilli);

    if (!liked) {
      createPostLike(props.authorId, props.postId)
      setLiked(true);
      setCount(count+1);
    } else {
      deletePostLike(props.authorId, props.postId)
      setLiked(false);
      setCount(count-1);
    }
  }

  return (
    <Stack alignItems="center"spacing={-1.5}>
      <DialogContentText align="center">
          {
            liked &&
            <IconButton aria-label="liked" onClick={handleSendLike}>
              <FavoriteTwoToneIcon />
            </IconButton>
          }
          {
            !liked &&
            <IconButton aria-label="like" onClick={handleSendLike}>
              <FavoriteBorderTwoToneIcon />
            </IconButton>
          }
      </DialogContentText>
      <DialogContentText align="center">
          {
            props.showCount &&
            <Typography component={'span'} sx={{ fontSize: 12 }} color="text.secondary">
              {count}
            </Typography>
          }
      </DialogContentText>
    </Stack>
  );
}
