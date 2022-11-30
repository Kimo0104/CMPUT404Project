import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

export default function BasicCard(props) {
  //props has summary, context
  //likes show the title of the post with a desc "User liked this post!"

  return (
    <Card sx={{ minWidth: 275 }}>
      <CardContent style={{backgroundColor: "#FAF9F6"}}>
        <Typography sx={{ fontSize: 18 }} color="text.primary" gutterBottom>
          {props.summary}
        </Typography>
        <Typography sx={{ mb: 1.5, frontSize: 14 }} color="text.secondary">
          {props.context}
        </Typography>
      </CardContent>
    </Card>
  );
}