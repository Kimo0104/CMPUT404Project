import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from 'axios';

export default function Login() {
    const [name, setName] = useState(''); 
    const [pass, setPass] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(name);
        axios({
            method: 'post',
            url: '/http://localhost:8000',
            data: {
              name: '',
              pass: ''
            }
          });
    }

    return (
        <div class="centered-form">
            <div class="login-form-container" >
                <h2>Login</h2>
                <form className="login-form" onSubmit={handleSubmit}>
                    <label htmlFor="name">username</label>
                    <input value={name} onChange={(e) => setName(e.target.value)}name="name" id="name" placeholder="username" />
                    <label htmlFor="password">password</label>
                    <input value={pass} onChange={(e) => setPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />
                    <button type="submit">Log In</button>
                </form>
                <div className="link-btn">
                <Link to="/register">Don't have an account? Register here.</Link>
                </div>

            </div>
        </div>
    )
}