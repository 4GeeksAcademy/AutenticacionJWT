const API = (path, opts={}) =>
  fetch(process.env.BACKEND_URL + path, {
    headers: { "Content-Type": "application/json", ...(opts.headers||{}) },
    ...opts
  });

export const signup = (email, password) =>
  API("/signup", { method: "POST", body: JSON.stringify({ email, password }) });

export const login = async (email, password) => {
  const res = await API("/token", { method: "POST", body: JSON.stringify({ email, password }) });
  const data = await res.json();
  if (res.ok) sessionStorage.setItem("token", data.access_token);
  return { ok: res.ok, data };
};

export const getPrivate = async () => {
  const token = sessionStorage.getItem("token");
  return API("/private", { headers: { Authorization: `Bearer ${token}` }});
};

export const logout = () => sessionStorage.removeItem("token");
