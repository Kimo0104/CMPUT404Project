import * as React from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import PublishText from "./PublishText.jsx"
import PublishImage from "./PublishImage.jsx"
export default function PublishTab(props) {
  // contains authorId
  const [value, setValue] = React.useState('one');

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  return (
    <Box >
      <Tabs value={value} onChange={handleChange} centered>
        <Tab value="one" label="Text Post" />
        <Tab value="two" label="Image Post" />
      </Tabs>
        {
            value === "one" && <PublishText 
              handleClickOpen={props.handleClickOpen} 
              handleCancel={props.handleCancel}
              handleError = {props.handleError}
              updateMyPosts={props.updateMyPosts} 
              page={props.page} 
              size={props.size}
              />
        }
        {
            value === "two" && <PublishImage 
              handleClickOpen={props.handleClickOpen} 
              handleCancel={props.handleCancel}
              handleError = {props.handleError}
              updateMyPosts={props.updateMyPosts} 
              page={props.page} 
              size={props.size}
              />
        }
    </Box>
  );
}