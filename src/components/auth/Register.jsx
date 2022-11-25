import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { createUser } from '../../APIRequests'


export default function Register() {
    const navigate = useNavigate();
    const [password, setPass] = useState('');
    const [confirmPassword, setConfirmedPass] = useState('');
    const [name, setName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            alert("Passwords don't match!");
        }
        else{
            let data = {
                // Do NOT change. Leave key as "displayName"
                "displayName": name,
                "password": password
            }
            async function register() {
                const isValid = await createUser(data);
                if (isValid){
                    navigate('/')
                }
                else{
                    alert("User already exists with this username.");
                }      
            }
            register()
        }
            
    };
    
    return (
        <div className="centered-form">
            <div className="register-form-container">
                <h2>Register</h2>
                <form className="register-form" onSubmit={handleSubmit}>
                    <label htmlFor="name">username</label>
                    <input value={name} onChange={(e) => setName(e.target.value)}name="name" id="name" placeholder="username" />

                    <label htmlFor="password">password</label>
                    <input value={password} onChange={(e) => setPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />

                    <label htmlFor="password">comfirm password</label>
                    <input value={confirmPassword} onChange={(e) => setConfirmedPass(e.target.value)} type="password" placeholder="********" id="confirmPassword" name="confirmPassword" />

                    <button type="submit">Register</button>
                </form>
                <div className="link-btn">
                <Link to="/">Already have an account? Click here to login.</Link>
                </div>
            </div>
        </div>
    )
}