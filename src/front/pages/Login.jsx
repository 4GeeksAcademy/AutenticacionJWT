import { useState } from "react";
import { login } from "../api";

export default function Login({ navigate }) {
  const [email,setEmail]=useState(""); const [password,setPassword]=useState("");
  const submit=async e=>{ e.preventDefault(); const {ok}=await login(email,password); if(ok) navigate("/private"); };
  return (
    <form onSubmit={submit}>
      <h2>Login</h2>
      <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="email" />
      <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="password" />
      <button>Entrar</button>
    </form>
  );
}
