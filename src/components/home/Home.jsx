import React, {useState} from "react";
import Grid from '@mui/material/Grid';
import TopBar from '../topbar/TopBar.jsx'
import HomeTab from '../homeTab/HomeTab'
import PublishButton from "./PublishButton.jsx";
import FriendRequestList from "../friendRequestList/FriendRequestList";
import { userIdContext } from '../../App';
import Profile from "../profile/Profile.jsx";
import SearchPage from "../search/SearchPage.jsx";
import Button from '@mui/material/Button';

// https://stackoverflow.com/a/64517088
export const AuthorIdContext = React.createContext({
  authorId: "1",
  setAuthorId: (value) => {}
})
export const ShowSearchContext = React.createContext({
  showSearch: false,
  setShowSearch: (value) => {}
})
export const QueryContext = React.createContext({
  query: ["", 1],
  setQuery: (value) => {}
})

export default function Home() {
  const { userId } = React.useContext(userIdContext);

  const [authorId, setAuthorId] = useState(localStorage.getItem("authorId") ? localStorage.getItem("authorId") : userId);
  const [showSearch, setShowSearch] = useState(localStorage.getItem("showSearch") ? localStorage.getItem("showSearch") : false);
  const [query, setQuery] = useState(localStorage.getItem("query") ? localStorage.getItem("query") : "");

  // https://stackoverflow.com/a/53455443
  const handleBack = () => {
    if (showSearch) {
      setAuthorId(userId);
      setShowSearch(false);
      localStorage.setItem("authorId", userId);
      localStorage.setItem("showSearch", false);
      localStorage.setItem("query", "");
    } else {
      setShowSearch(true);
    }
  }
  let leftPane = "";
  if (showSearch) {
    leftPane = <SearchPage />;
  } else {
    leftPane = <Profile authorId={authorId}/>;
  }

  return (
    <AuthorIdContext.Provider value={{authorId, setAuthorId}}>
      <ShowSearchContext.Provider value={{showSearch, setShowSearch}}>
        <QueryContext.Provider value={{query, setQuery}}>
          <div>
            <TopBar/>
            <div>
              <Grid container>
                <Grid item xs={4}>
                  <Grid container rowSpacing={2}>
                    <Grid item xs={12}></Grid>
                    <Grid item xs={12}></Grid>
                    <Grid item xs={2}></Grid>
                    <Grid item>
                      <PublishButton/>
                      <FriendRequestList authorId={userId} />
                    </Grid>
                    <Grid item xs={2}></Grid>
                  </Grid>
                </Grid>
                <Grid item xs={8}>
                  <Grid container spacing={2}>
                    <Grid item xs={8}>
                        <HomeTab authorId={userId}/>
                    </Grid>
                    <Grid item xs={1}>
                    </Grid>
                    <Grid item xs={2}>
                    <Grid container spacing={2}>
                      <Grid item xs={12}></Grid>
                      <Grid item xs={12}>
                        {(authorId !== userId || showSearch) &&
                          <Button onClick={handleBack}>Back</Button>
                        }
                        {leftPane}
                        </Grid>
                      </Grid>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </div>
          </div>
        </QueryContext.Provider>
      </ShowSearchContext.Provider>
    </AuthorIdContext.Provider>
  )
}
