import { For, Show,createSignal } from "solid-js"
import "./assets/css/fastlist.css"
import { config } from "/src/assets/config.js"

let fastlist_config = config["fastlist"]

const [fastLogo,setFastLogo] = createSignal(0)
const [fastListConfig,setFastListConfig] = createSignal(0)
// 跳轉頁面
function jumpPage(href){
    window.open(href)
}

// 便捷访问栏logo显示
function FastLogo(){
    return (
        <Show when={ fastLogo() == 1 } >
            <div class = "fastlogo_box">
                <img src = {fastlist_config[fastListConfig()][1]}/>
                <div class="fastlogo_text" >{fastlist_config[fastListConfig()][2]}</div>
            </div>
        </Show>
    )
}

// 便捷访问栏主体
function Fastlist(){
    return (
        <div class="fast_visit">
            <For each={fastlist_config} fallback={<div></div>}>
                {
                    (item,index)=>{
                        return (
                        <div class="link_url" >
                            <img 
                            class = "link_url_img"
                            alt = {item[2]}
                            onMouseout = {()=>{setFastLogo(0)}}
                            onMouseover = {()=>{setFastLogo(1),setFastListConfig(index)}}
                            onClick = {()=>jumpPage(item[0])}
                            src = {item[1]}
                            />
                        </div>
                        )
                    }
                }
            </For>
        </div>
    )
}

function Fast(){
    return(
        <>
            <Fastlist/>
            <FastLogo/>
        </>
    )
}

export default Fast