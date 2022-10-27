import './App.css';
import React, { useState } from "react";
import { BrowserRouter, Routes, Route} from 'react-router-dom';
// import Login from './components/login/Login.jsx'
import Home from './components/home/Home.jsx'
import Login from './components/auth/Login.jsx'
import Register from './components/auth/Register.jsx'

function App() {
  // const [currentForm, setCurrentForm] = useState('login');
  // const toggleForm = (formName) => {
  //   setCurrentForm(formName);
  // }
  return (
    <BrowserRouter>
      <div className="App">
        <div className = "content">
            {/* {
              currentForm === "login" ? <Login onFormSwitch={toggleForm} /> : <Register onFormSwitch={toggleForm} />
            } */}
            <Routes>
              <Route path="/" element={<Login/>} exact/>
              <Route path="/register" element={<Register/>}/>
              <Route path="/home" element={<Home/>}/>
            </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
