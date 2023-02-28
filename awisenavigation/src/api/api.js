import axios from "/src/requests/axios.js"

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
    let parame = search["keys"]+"="+value
    window.open(search["url"]+"?"+parame)
}
