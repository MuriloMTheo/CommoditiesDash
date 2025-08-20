import axios from "axios";

const api = axios.create({
    baseURL: "https://web-production-b323.up.railway.app/commodities",
});
export default api