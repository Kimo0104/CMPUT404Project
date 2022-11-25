import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser, authUser } from '../../APIRequests';
import { userIdContext } from '../../App'

export default function Login() {

    var { setUserId } = React.useContext(userIdContext);

    const navigate = useNavigate();
    const [name, setName] = useState(''); 
    const [pass, setPass] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(name); 
        console.log(pass);

        let data = {
            "username": name,
            "password": pass
        };

        async function login() {
            const token = await loginUser(data);
            if (token){
                localStorage.setItem("token", JSON.stringify(token));
                const tokenFromStorage = (JSON.parse(localStorage.getItem("token", JSON.stringify(token)))).jwt

                const dataForAuthUser = {
                    "userToken": tokenFromStorage
                }
                const userID = await authUser(dataForAuthUser);
                if (userID){
                    let id = String(userID.id).replace(/-/g,"");
                    setUserId(id);
                    localStorage.setItem("userId", id);
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
                <Link to="/register">Don't have an account? Click here to register.</Link>
                </div>

            </div>
        </div>
    )
}