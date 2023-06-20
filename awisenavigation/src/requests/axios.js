import axios from "axios";
import { AWMsg } from "/src/assembly/awiseUI/awiseUI"

const request = axios.create({
    baseURL: "https://homeapi.fzass.com",
    timeout: 3000,
    withCredentials: true,
    headers: {
        "Content-Type": "multipart/form-data",
        "Access-Control-Allow-Origin": "*",
        }
})

// 请求拦截器
request.interceptors.request.use(
    function (config) {
        // 在发送请求之前做些什么
        return config;
    },
    function (error) {
        // 对请求错误做些什么
        AWMsg("error",error.message)
        return Promise.reject(error);
    }
)

// 响应拦截器
request.interceptors.response.use(
    function (response) {
        // 2xx 范围内的状态码都会触发该函数。
        // 对响应数据做点什么
        return response;
    }, 
    function (error) {
        // 超出 2xx 范围的状态码都会触发该函数。
        // 对响应错误做点什么
        AWMsg("error",error.message)
        return Promise.reject(error);
    }
)
export default request