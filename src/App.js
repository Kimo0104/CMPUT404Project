import './App.css';
import React from "react";
import Login from './components/auth/Login.jsx'
import Register from './components/auth/Register.jsx'
import { BrowserRouter, Routes, Route, Navigate} from 'react-router-dom';
import Home from './components/home/Home.jsx';
import Profile from './components/profile/Profile.jsx';
import ManageProfile from './components/profile/ManageProfile.jsx';
import SearchPage from './components/search/SearchPage';
import Follow from './components/follow/Follow.jsx'
import FriendRequestList from './components/friendRequestList/FriendRequestList.jsx'
import axios from 'axios';
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export const userIdContext = React.createContext({
  userId: localStorage.getItem("userId") ? localStorage.getItem("userId") : "1",
  setUserId: (value) => {}
  });

function App() {

  const [userId, setUserId] = React.useState(localStorage.getItem("userId") ? localStorage.getItem("userId") : "1");
  
  return (
    <userIdContext.Provider value={{userId, setUserId}}>
      <BrowserRouter>
        <div className="App">
          <div className = "content">
              {/* {
                currentForm === "login" ? <Login onFormSwitch={toggleForm} /> : <Register onFormSwitch={toggleForm} />
              } */}
              <Routes>
                <Route path="/" element={<Login/>} exact/>
                <Route path="/register" element={<Register/>}/>
                <Route path="home" element={<Home unlisted={false}/>}/>
                <Route path="profile" element={<Navigate to={`/profile/${userId}`}/>}/>
                <Route path={"profile/:exact"} element={<Profile userId={userId}/>}/>
                <Route path="search" element={<SearchPage userId={userId}/>}/>
                <Route path={`profile/${userId}/manage`} element={<ManageProfile userId={userId}/>}/>
                <Route path="follow" element={<Follow authorId={userId} foreignAuthorId="2" />}/>
                <Route path="friendRequestList" element={<FriendRequestList authorId={userId} />}/>
                <Route path="unlisted" element={<Home unlisted={true}/>}/>
              </Routes>
          </div>
        </div>
      </BrowserRouter>
    </userIdContext.Provider>
  );
}

export default App;
