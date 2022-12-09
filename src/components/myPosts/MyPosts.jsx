import * as React from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import Pagination from '@mui/material/Pagination';

import MyPost from './MyPost'

export default function BasicStack(props) {
  //props contains authorId

  var key = 1;

  return (
    <Box sx={{ width: '100%', marginTop: 2}}>
      <Stack alignItems="center">
        <Pagination sx={{marginBottom:1, marginLeft: 'auto', marginRight: 'auto'}} count={props.numPages} onChange={props.handlePostsChange}/>
      </Stack>
      <Stack spacing={2} divider={<Divider orientation="horizontal" flexItem />}>
        {
          props.inbox.map((item) => (
            <MyPost 
              item={item} 
              key={key++} 
              updateMyPosts={props.updateMyPosts} 
              page={props.page} 
              size={props.size}
              />
            ))
        }
      </Stack>
    </Box>
  );
}