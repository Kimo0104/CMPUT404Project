import React, {useState} from "react";
import Grid from '@mui/material/Grid';
import TopBar from '../topbar/TopBar.jsx'
import HomeTab from '../homeTab/HomeTab'
import PublishButton from "./PublishButton.jsx";
import FriendRequestList from "../friendRequestList/FriendRequestList";
import { userIdContext } from '../../App';
import Profile from "../profile/Profile.jsx";
import SearchPage from "../search/SearchPage.jsx";
import IconButton from '@mui/material/Button';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import Divider from '@mui/material/Divider';
import { getPublicPosts } from '../../APIRequests'

// https://stackoverflow.com/a/64517088
export const AuthorIdContext = React.createContext({
  authorId: "1",
  setAuthorId: (value) => {}
})
export const ShowSearchContext = React.createContext({
  showSearch: "false",
  setShowSearch: (value) => {}
})
export const QueryContext = React.createContext({
  query: ["", 1],
  setQuery: (value) => {}
})

export default function Home() {
  const { userId } = React.useContext(userIdContext);

  const [authorId, setAuthorId] = useState(localStorage.getItem("authorId") ? localStorage.getItem("authorId") : userId);
  const [showSearch, setShowSearch] = useState(localStorage.getItem("showSearch") ? localStorage.getItem("showSearch") : "false");
  const [query, setQuery] = useState(localStorage.getItem("query") ? localStorage.getItem("query") : "");

  // Code for PublishTab and Myposts
  const size = 5;
  const [numPages, setNumPages] = React.useState(0);
  const [page, setPage] = React.useState(1);

  const handlePostsChange = (event, value) => {
    setPage(value);
    updateMyPosts(value, size);
  };

  const [inbox, setInbox] = React.useState([]);

  const updateMyPosts = (page, size) => {
    // State change will cause component re-render
    async function fetchPublicPosts() {
      const output = await getPublicPosts(authorId, page, size);
      if (output.posts.length == 0) { return; }
      setInbox(output.posts);
      setNumPages(Math.ceil(output.count/size));
    }
    fetchPublicPosts();
  }

  React.useEffect(() => {
    updateMyPosts(page, size);
    // disable this warning because updateMyPosts has to be used outside of the useEffect as well
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // https://stackoverflow.com/a/53455443
  const handleBack = () => {
    if (showSearch == "true") {
      setAuthorId(userId);
      setShowSearch("false");
      localStorage.setItem("authorId", userId);
      localStorage.setItem("showSearch", "false");
      localStorage.setItem("query", "");
    } else {
      setShowSearch("true");
    }
  }
  let rightPane = "";
  if (showSearch == "true") {
    rightPane = <SearchPage />;
  } else {
    rightPane = <Profile authorId={authorId}/>;
  }

  return (
    <AuthorIdContext.Provider value={{authorId, setAuthorId}}>
      <ShowSearchContext.Provider value={{showSearch, setShowSearch}}>
        <QueryContext.Provider value={{query, setQuery}}>
          <div>
            <TopBar/>
            <div>
              <Grid container>
                <Grid item xs={3}>
                  <Grid container rowSpacing={3} sx={{ width: '90%', marginRight: 3, marginLeft: 3, marginTop: 3}}>
                    <Grid item xs={12} align="center" justify="top">
                      <PublishButton 
                        updateMyPosts={updateMyPosts} 
                        page={page} 
                        size={size} 
                        handlePostsChange={handlePostsChange} 
                        setInbox={setInbox}
                        />
                    </Grid>
                    <Grid item xs={12} align="center" justify="center">
                      <Divider orientation="horizontal" flexItem sx={{ mr: "-1px" }} />
                    </Grid>
                    <Grid item xs={12} align="center" justify="center">
                      <FriendRequestList authorId={userId} />
                    </Grid>
                  </Grid>
                </Grid>
                <Divider orientation="vertical" flexItem sx={{ mr: "-1px", minHeight: 700}} />
                <Grid item xs={5.5}>
                  <HomeTab 
                    authorId={userId} 
                    inbox={inbox} 
                    numPages={numPages} 
                    page={page} 
                    size={size} 
                    handlePostsChange={handlePostsChange}
                    updateMyPosts={updateMyPosts}
                    />
                </Grid>
                <Divider orientation="vertical" flexItem sx={{ mr: "-1px", minHeight: 700 }} />
                <Grid item xs={3.5}>
                {(authorId !== userId || showSearch == "true") &&
                        <Grid container>
                          <Grid item xs={2}>
                            <IconButton onClick={handleBack} size="medium">
                              <ArrowBackIcon/>
                            </IconButton>
                          </Grid>
                        </Grid>
                        }
                {rightPane}
                </Grid>
              </Grid>
            </div>
          </div>
        </QueryContext.Provider>
      </ShowSearchContext.Provider>
    </AuthorIdContext.Provider>
  )
}
