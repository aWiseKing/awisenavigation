import axios from "/src/requests/axios.js"

import requestIp from "request-ip"

// 将get关键字组合
function combineKeyIntoFict(keys,values){
    let tmp = []
    for(let num in keys){
        tmp.push(keys[num]+"="+values[num])
    }

    return tmp.join("&")
}
// 发送get搜索请求
export function sendGetSearch(search_config_web,search_web,value){
    let search = search_config_web[search_web]
    if(search["getid"] == true){
        let parame = search["keys"]+"="+value
        window.open(search["url"]+"?"+parame)
    }else{
        window.open(search["url"]+value)
    }
}

// 发送post向后端记录搜索关键词
export function sendWebBackSearchKeyWord(search_engine,value){
    axios.post("/search",{
        value:value,
        search_engine:search_engine
    })
}
