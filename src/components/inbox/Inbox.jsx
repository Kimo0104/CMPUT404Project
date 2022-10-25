import * as React from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';

import TextPost from './TextPost'
import { getInbox } from '../../APIRequests'

export default function BasicStack(props) {
  //props contains authorId

  var key = 1;
  const [inbox, setInbox] = React.useState([]);

  const updateInbox = (page, size) => {
    // State change will cause component re-render
    async function fetchInbox() {
      const output = await getInbox(props.authorId, page, size);
      console.log(output);
      var inboxItems = [];
      for (let i = 0; i < output.length; ++i) {
        let inboxItem = output[i];
        if (inboxItem.type === "post") {
          inboxItems.push(inboxItem);
        }
      }
      setInbox(inboxItems);
    }
    fetchInbox();
  }
  
  React.useEffect(() => {
    updateInbox(1, 10);
    // disable this warning because updateInbox has to be used outside of the useEffect as well
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Box sx={{ width: '100%', marginRight: 3, marginLeft: 3}}>
      <Stack spacing={2} divider={<Divider orientation="horizontal" flexItem />}>
        {
          inbox.map((item) => (
            <TextPost title={item.title} content={item.content} authorId={item.author} key={key++}/>
          ))
        }
      </Stack>
    </Box>
  );
}