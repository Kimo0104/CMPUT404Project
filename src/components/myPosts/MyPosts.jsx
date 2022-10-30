import * as React from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import Pagination from '@mui/material/Pagination';

import MyPost from './MyPost'
import { getPublicPosts } from '../../APIRequests'

export default function BasicStack(props) {
  //props contains authorId

  var key = 1;

  const size = 5;
  const [numPages, setNumPages] = React.useState(0);
  const [page, setPage] = React.useState(1);

  const handleChange = (event, value) => {
    setPage(value);
    updateMyPosts(value, size);
  };

  const [inbox, setInbox] = React.useState([]);

  const updateMyPosts = (page, size) => {
    // State change will cause component re-render
    async function fetchPublicPosts() {
      const output = await getPublicPosts(props.authorId, page, size);
      console.log(output);
      if (output.posts.length == 0) { return; }
      setInbox(output.posts);
      setNumPages(Math.ceil(output.count/size));
    }
    fetchPublicPosts();
  }
  
  React.useEffect(() => {
    updateMyPosts(page, size);
    // disable this warning because updateMyPosts has to be used outside of the useEffect as well
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Box sx={{ width: '100%', marginTop: 2}}>
      <Stack alignItems="center">
        <Pagination sx={{marginBottom:1, marginLeft: 'auto', marginRight: 'auto'}} count={numPages} onChange={handleChange}/>
      </Stack>
      <Stack spacing={2} divider={<Divider orientation="horizontal" flexItem />}>
        {
          inbox.map((item) => (
            <MyPost title={item.title} content={item.content} key={key++}/>
            ))
        }
      </Stack>
    </Box>
  );
}