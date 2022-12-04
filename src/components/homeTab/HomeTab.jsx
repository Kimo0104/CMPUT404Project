/* eslint-disable */
import * as React from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';

import Inbox from '../inbox/Inbox';
import MyPosts from '../myPosts/MyPosts';
import GithubEvents from '../githubEvents/GithubEvents';

import { getAuthor } from '../../APIRequests'

export default function TabsWrappedLabel(props) {
  // contains authorId
  const [value, setValue] = React.useState('one');

  const [author, setAuthor] = React.useState(null);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  
  React.useEffect(() => {
    async function fetchAuthor() {
      const fetchedAuthor = await getAuthor(props.authorId);
      setAuthor(fetchedAuthor);
    }
    fetchAuthor();
  }, []);

  return (
    <Box sx={{ width: '90%', marginRight: 3, marginLeft: 3, marginTop: 3, marginBottom: 3}}>
      <Tabs value={value} onChange={handleChange} centered>
        <Tab value="one" label="Inbox" />
        <Tab value="two" label="My Posts" />
        {
          author && author.github && author.github !== "" && <Tab value="three" label="Github Activity"/>
        }
      </Tabs>
        {
          value === "one" && <Inbox authorId={props.authorId}/>
        }
        {
          value === "two" && <MyPosts authorId={props.authorId} inbox={props.inbox} numPages={props.numPages} handlePostsChange={props.handlePostsChange}/>
        }
        {
          value === "three" && <GithubEvents github={author.github}/>
        }
    </Box>
  );
}