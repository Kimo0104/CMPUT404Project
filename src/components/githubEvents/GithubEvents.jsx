import * as React from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import Pagination from '@mui/material/Pagination';

import GithubEvent from './GithubEvent'
import { getPublicPosts, getGithubEvents } from '../../APIRequests'

export default function BasicStack(props) {
  //props contains authorId

  var key = 1;

  const size = 10;
  const [numPages, setNumPages] = React.useState(3);
  const [page, setPage] = React.useState(1);

  const handleChange = (event, value) => {
    setPage(value);
    updateGithubEvents(value, size);
  };

  const [events, setEvents] = React.useState([]);

  const updateGithubEvents = (page, size) => {
    // State change will cause component re-render
    async function fetchGithubActivity() {
      const output = await getGithubEvents('Kimo0104', page, size);
      if (output.length == 0) { return; }
      setEvents(output);
      setNumPages(3);
    }
    fetchGithubActivity();
  }
  
  React.useEffect(() => {
    updateGithubEvents(page, size);
    // disable this warning because updateGithubEvents has to be used outside of the useEffect as well
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Box sx={{ width: '100%', marginTop: 2}}>
      <Stack alignItems="center">
        <Pagination sx={{marginBottom:1, marginLeft: 'auto', marginRight: 'auto'}} count={numPages} onChange={handleChange}/>
      </Stack>
      <Stack spacing={1} divider={<Divider orientation="horizontal" flexItem />}>
        {
          events.map((item) => (
            <GithubEvent item={item} key={key++}/>
            ))
        }
      </Stack>
    </Box>
  );
}