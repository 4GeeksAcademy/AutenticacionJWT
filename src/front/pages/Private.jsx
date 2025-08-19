import { useEffect, useState } from "react";
import { getPrivate } from "../api";

export default function Private({ navigate }) {
  const [data,setData]=useState(null);
  useEffect(()=>{
    const token = sessionStorage.getItem("token");
    if(!token) return navigate("/login");
    getPrivate().then(async res=>{
      if(res.ok) setData(await res.json());
      else navigate("/login");
    });
  },[]);
  if(!data) return <p>Cargando...</p>;
  return <pre>{JSON.stringify(data, null, 2)}</pre>;
}
