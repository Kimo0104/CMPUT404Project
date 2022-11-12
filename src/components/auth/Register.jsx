import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { createUser } from '../../APIRequests'


export default function Register() {
    // const [email, setEmail] = useState('');
    const [password, setPass] = useState('');
    const [confirmPassword, setConfirmedPass] = useState('');
    const [name, setName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            alert("Passwords don't match");
        }
        else{
            let data = {
                // Do NOT change. Leave key as "displayName"
                "displayName": name,
                "email": email,
                "password": pass
            }
            createUser(data);
            navigate('/login')
        }
            
    };
    
    return (
        <div className="centered-form">
            <div className="register-form-container">
                <h2>Register</h2>
                <form className="register-form" onSubmit={handleSubmit}>
                    <label htmlFor="name">username</label>
                    <input value={name} onChange={(e) => setName(e.target.value)}name="name" id="name" placeholder="username" />

                    {/* <label htmlFor="email">email</label>
                    <input value={email} onChange={(e) => setEmail(e.target.value)}type="email" placeholder="youremail@gmail.com" id="email" name="email" /> */}

                    <label htmlFor="password">password</label>
                    <input value={pass} onChange={(e) => setPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />

                    <label htmlFor="password">comfirm password</label>
                    <input value={pass} onChange={(e) => setConfirmedPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />

                    <button type="submit">Register</button>
                </form>
                <div className="link-btn">
                <Link to="/">Don't have an account? Register here.</Link>
                </div>
            </div>
        </div>
    )
}