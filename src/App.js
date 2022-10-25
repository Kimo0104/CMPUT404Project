import './App.css';
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import Login from './components/login/Login.jsx'
import Home from './components/home/Home.jsx'
function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <div className = "content">
            <Routes>
              <Route path="/" element={<Login/>}/>
              <Route path="home" element={<Home/>}/>
            </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
