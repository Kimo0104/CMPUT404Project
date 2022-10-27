import * as React from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import Pagination from '@mui/material/Pagination';

import InboxItem from './InboxItem'
import TextPost from './TextPost'
import { getInbox } from '../../APIRequests'

export default function BasicStack(props) {
  //props contains authorId

  var key = 1;

  const size = 5;
  const [numPages, setNumPages] = React.useState(0);
  const [page, setPage] = React.useState(1);

  const handleChange = (event, value) => {
    setPage(value);
    updateInbox(value, size);
  };

  const [inbox, setInbox] = React.useState([]);

  const updateInbox = (page, size) => {
    // State change will cause component re-render
    async function fetchInbox() {
      const output = await getInbox(props.authorId, page, size);
      console.log(output);
      if (output == "{Nothing to show}") { return; }
      setInbox(output.inbox);
      setNumPages(Math.ceil(output.count/size));
    }
    fetchInbox();
  }
  
  React.useEffect(() => {
    updateInbox(page, size);
    // disable this warning because updateInbox has to be used outside of the useEffect as well
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Box sx={{ width: '100%', marginRight: 3, marginLeft: 3, marginTop: 3}} align="center">
      <Stack alignItems="center">
        <Pagination sx={{marginBottom:1, marginLeft: 'auto', marginRight: 'auto'}} count={numPages} onChange={handleChange}/>
      </Stack>
      <Stack spacing={2} divider={<Divider orientation="horizontal" flexItem />}>
        {
          inbox.map((item) => (
            <InboxItem authorId={props.authorId} item={item} key={key++}/>
            ))
        }
      </Stack>
    </Box>
  );
}