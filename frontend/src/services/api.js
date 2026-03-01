import axios from "axios";

const API = axios.create({
  baseURL: "https://pharma-crm-7gxm.onrender.com",
});

export default API;