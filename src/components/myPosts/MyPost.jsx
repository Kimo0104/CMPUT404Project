import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';

export default function BasicCard(props) {
  //props contains title, content
  return (
    <Card sx={{ minWidth: 275 }}  style={{backgroundColor: "#F9F0C1"}}>
      <Grid>
        <Grid container spacing={1}>
          <Grid item xs={11}>
          </Grid>
          <Grid item xs>
            <MoreHorizIcon/>
          </Grid>
        </Grid>
      </Grid>
      <CardContent>
        <Typography sx={{ fontSize: 32 }} color="text.primary" gutterBottom>
          {props.title}
        </Typography>
        <Typography sx={{ mb: 1.5, frontSize: 24 }} color="text.secondary">
          {props.content}
        </Typography>
      </CardContent>
    </Card>
  );
}