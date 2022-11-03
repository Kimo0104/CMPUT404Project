import * as React from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';

import Inbox from '../inbox/Inbox';
import MyPosts from '../myPosts/MyPosts';

export default function TabsWrappedLabel(props) {
  // contains authorId
  const [value, setValue] = React.useState('one');

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: '100%', marginRight: 3, marginLeft: 3, marginTop: 3}}>
      <Tabs value={value} onChange={handleChange} centered>
        <Tab value="one" label="Inbox" />
        <Tab value="two" label="My Posts" />
      </Tabs>
        {
          value == "one" && <Inbox authorId={props.authorId}/>
        }
        {
          value == "two" && <MyPosts authorId={props.authorId}/>
        }
    </Box>
  );
}