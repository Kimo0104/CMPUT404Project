import './App.css';
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import Login from './components/login/Login.jsx'
import Home from './components/home/Home.jsx'
import Follow from './components/follow/Follow.jsx'
import FriendRequestList from './components/friendRequestList/FriendRequestList.jsx'
function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <div className = "content">
            <Routes>
              <Route path="/" element={<Login/>}/>
              <Route path="home" element={<Home/>}/>
              <Route path="follow" element={<Follow authorId="3" foreignAuthorId="2" />}/>
              <Route path="friendRequestList" element={<FriendRequestList authorId="2" />}/>
            </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
