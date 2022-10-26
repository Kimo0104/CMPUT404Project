import './App.css';
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import Login from './components/login/Login.jsx'
import Home from './components/home/Home.jsx'
import Follow from './components/follow/Follow.jsx'
function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <div className = "content">
            <Routes>
              <Route path="/" element={<Login/>}/>
              <Route path="home" element={<Home/>}/>
              <Route path="follow" element={<Follow authorId="2" foreignAuthorId="1" />}/>
            </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
