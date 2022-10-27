/* eslint-disable */
import * as React from 'react';
import DialogContentText from '@mui/material/DialogContentText';
import FavoriteBorderTwoToneIcon from '@mui/icons-material/FavoriteBorderTwoTone';
import FavoriteTwoToneIcon from '@mui/icons-material/FavoriteTwoTone';
import IconButton from '@mui/material/IconButton';

import { getAuthorPostLike, createPostLike, deletePostLike } from '../../APIRequests'

export default function FormDialog(props) {
  //props has authorId, postId
  const [debounce, setDebounce] = React.useState((new Date()).getTime());
  const [liked, setLiked] = React.useState(false);

  React.useEffect(() => {
    async function loadInfo() {
      const liked = await getAuthorPostLike(props.authorId, props.postId);
      setLiked(liked);
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
    } else {
      deletePostLike(props.authorId, props.postId)
      setLiked(false);
    }
  }

  return (
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
  );
}
