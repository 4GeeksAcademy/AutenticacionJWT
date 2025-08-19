import { useState } from "react";
import { signup } from "../api";

export default function Signup({ navigate }) {
  const [email,setEmail]=useState(""); const [password,setPassword]=useState("");
  const submit=async e=>{ e.preventDefault(); const r=await signup(email,password); if(r.ok) navigate("/login"); };
  return (
    <form onSubmit={submit}>
      <h2>Signup</h2>
      <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="email" />
      <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="password" />
      <button>Crear</button>
    </form>
  );
}
