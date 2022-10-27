import './App.css';
import { BrowserRouter, Routes, Route, Navigate} from 'react-router-dom';
import Login from './components/login/Login.jsx';
import Home from './components/home/Home.jsx';
import Profile from './components/profile/Profile.jsx';
import ManageProfile from './components/profile/ManageProfile.jsx';
import SearchPage from './components/search/SearchPage';
import Follow from './components/follow/Follow.jsx'
import FriendRequestList from './components/friendRequestList/FriendRequestList.jsx'

function App() {

  const userId = "test_author";
  
  return (
    <BrowserRouter>
      <div className="App">
        <div className = "content">
            <Routes>
              <Route path="/" element={<Login/>}/>
              <Route path="home" element={<Home/>}/>
              <Route path="profile" element={<Navigate to={`/profile/${userId}`}/>}/>
              <Route path={"profile/:exact"} element={<Profile userId={userId}/>}/>
              <Route path="search" element={<SearchPage userId={userId}/>}/>
              <Route path={`profile/${userId}/manage`} element={<ManageProfile userId={userId}/>}/>
              <Route path="follow" element={<Follow authorId="3" foreignAuthorId="2" />}/>
              <Route path="friendRequestList" element={<FriendRequestList authorId="2" />}/>
            </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
