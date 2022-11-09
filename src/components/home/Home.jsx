import React from "react";
import Grid from '@mui/material/Grid';
import TopBar from '../topbar/TopBar.jsx'
import HomeTab from '../homeTab/HomeTab'
import PublishButton from "./PublishButton.jsx";
export default function Home() {
  return (
    <div>
      <TopBar/>
        <div>
          <Grid container spacing={2}>
            <Grid item xs={2}>
            </Grid>
            <Grid item xs={8}>
                <HomeTab authorId={1}/>
            </Grid>
            <Grid item xs={2}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
              </Grid>
                <PublishButton/>
              </Grid>
            </Grid>
          </Grid>
        </div>
    </div>
  )
}
