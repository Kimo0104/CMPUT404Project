import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

export default function BasicCard(props) {
  //props has summary, context
  //likes show the title of the post with a desc "User liked this post!"

  return (
    <Card sx={{ minWidth: 275 }} style={{backgroundColor: "#FAF9F6"}}> 
      <Typography sx={{ fontSize: 18, marginLeft: 3 }} color="text.primary" align='left'>
        {props.summary}: {props.context}
      </Typography>
    </Card>
  );
}