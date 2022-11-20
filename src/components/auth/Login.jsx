import { ConnectingAirportsOutlined } from "@mui/icons-material";
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser, authUser } from '../../APIRequests';
import { usernameContext, passwordContext } from "../../App";

export default function Login() {
    const navigate = useNavigate();
    const [name, setName] = useState(''); 
    const [pass, setPass] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        let data = {
            "username": name,
            "password": pass
        };

        async function login() {
            const token = await loginUser(data);
            if (token){
                localStorage.setItem("token", JSON.stringify(token));
                const tokenFromStorage = (JSON.parse(localStorage.getItem("token", JSON.stringify(token)))).jwt
                console.log(tokenFromStorage)

                const dataForAuthUser = {
                    "userToken": tokenFromStorage
                }
                const userID = await authUser(dataForAuthUser);
                if (userID){
                    console.log(userID)
                    navigate('/home');
                }
            }
        }
        login()

    }

    return (
        <div className="centered-form">
            <div className="login-form-container" >
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