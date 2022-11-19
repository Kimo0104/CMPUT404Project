import React from "react";
import Grid from '@mui/material/Grid';
import TopBar from '../topbar/TopBar.jsx'
import HomeTab from '../homeTab/HomeTab'
import PublishButton from "./PublishButton.jsx";
import FriendRequestList from "../friendRequestList/FriendRequestList";
import { userIdContext } from '../../App';
export default function Home() {
  const userId = React.useContext(userIdContext);
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
                <FriendRequestList authorId={userId} />
              </Grid>
            </Grid>
          </Grid>
        </div>
    </div>
  )
}
