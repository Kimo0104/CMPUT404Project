import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from 'axios';


export default function Register() {
    const [pass, setPass] = useState('');
    const [name, setName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(name);
    };
    
    return (
        <div class="centered-form">
            <div className="register-form-container">
                <h2>Register</h2>
                <form className="register-form" onSubmit={handleSubmit}>
                    <label htmlFor="name">username</label>
                    <input value={name} onChange={(e) => setName(e.target.value)}name="name" id="name" placeholder="username" />
                    <label htmlFor="password">password</label>
                    <input value={pass} onChange={(e) => setPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />
                    <button type="submit">Register</button>
                </form>
                <div className="link-btn">
                <Link to="/">Don't have an account? Register here.</Link>
                </div>
            </div>
        </div>
    )
}