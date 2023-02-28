import { createSignal,createEffect,onMount,For, Show } from "solid-js"
import { store,setStore } from "/src/store/store"
import { render } from "solid-js/web"
import { config } from "/src/assets/config.js"
import { sendGetSearch } from "/src/api/api.js"
import "./assets/css/search.css"

let search_config = config["search"]
let search_config_web = search_config["web"]
const [searchValue,setSearchValue] = createSignal("")
const [searchType,setSearchType] = createSignal(0)
const [recentSearches,setRrecentSearches] = createSignal([])
const [searchTipType,setSearchTipType] = createSignal(0)

// 搜索发送
function sendSearch(search_config_web,search_web,value){
    sendGetSearch(search_config_web,search_web,value)
    let recent_searches = recentSearches()
    if(recent_searches.includes(value)){
        let index = recent_searches.indexOf(value)
        recent_searches.splice(index, 1)
    }
    recent_searches.splice(0,0,value)
    recent_searches.splice(5, 1)
    setRrecentSearches(recent_searches)
    window.localStorage.setItem("recent_searches",JSON.stringify(recentSearches()))
}

// 回车搜索
function enterSearch(e,search_config_web,search_web,value){
    if(e.key == "Enter"){
        sendSearch(search_config_web,search_web,value)
    }
}

// 搜索背景层次
function SearchBg(){
    return (
        <div onClick={()=>{setSearchType(0);setSearchValue("");setSearchTipType(0)}} class={searchType()==0?"search_bg":"search_bg search_bg_play"}></div>
    )
}

// 搜索提示框 鼠标选中时弹出最近搜索内容 输入内容后更新为用户对相关内容的多次搜索
 // 提示框本体
function SearchTips(){
    return (
        
            <div class =  "search_tips" style={`height:${searchTipType()==0?0:recentSearches().length*32}px;`}>
                <Show when={searchTipType() == 1}>
                <For each={recentSearches()} fallback={<div></div>}>
                    {(item)=>{return (<div onClick={()=>{setSearchValue(item),sendSearch(search_config_web,store()["search_web"],searchValue()),setSearchTipType(0)}} class="search_tip" >{item}</div>)}}
                </For>
                </Show>
            </div>

        )
}

// 搜索引擎快速切换框
export function SearchMode(){
    const [searchMode,setSearchMode]=createSignal(search_config_web[store()["search_web"]])
    const [searchModeMenu,setSearchModeMenu]=createSignal(0)
    return (
        <div class="search_web_set_choice">
            <div class="search_web_set_choice_button" name="baidu_search" id="search_web_set_choice_button"
                onBlur={()=>setSearchModeMenu(0)} onFocus={()=>setSearchModeMenu(1)} tabindex="0">
                    <img src = {searchMode()["icon"]}/>
            </div>
            
            <div style={`height:${searchModeMenu()==1?130:0}px;padding:${searchModeMenu()==1?"3px 3px 3px 3px":"0px 0px 0px 0px"}`} class="search_web_set_choice_box">
                <For each={search_config_web} fallback={<div></div>}>
                    {(item,index)=>{
                            let search_choice_ico
                            // 修改搜索引擎store参数
                            function setSearchModeF(id_num){
                                let search_web = store()
                                search_web["search_web"] = id_num
                                return search_web
                            }
                            // 修改搜索引擎
                            function setSearchModeA(){
                                setStore(()=>setSearchModeF(index()))
                                setSearchMode(search_config_web[store()["search_web"]])
                            }
                            
                            return (<div class="search_choice_ico" name="baidu_search" id="baidu_search" ref = {search_choice_ico}
                                onFocus={()=>setSearchModeA()} tabindex="0">
                                    <img src = {item["icon"]}/>
                            </div>
                            )
                        }
                    }
                </For>
            </div>
        </div>
    )
}

// 搜索框
export function SearchBox(){
    let search

    createEffect(()=>{
        search.value = searchValue()
    })

    onMount(()=>{
        setRrecentSearches(window.localStorage.getItem("recent_searches") == undefined?[]:JSON.parse(window.localStorage.getItem("recent_searches")))
      
    })

    return (
        <input 
            ref = {search} 
            type="text" 
            class = "search" 
            placeholder="此处输入关键字进行搜索" 
            onFocus={()=>{setSearchType(1),setSearchTipType(1)}}
            onkeydown={(e)=>enterSearch(e,search_config_web,store()["search_web"],searchValue())}
            onInput={()=>setSearchValue(()=>search.value)}
        >
        </input>
    )
}

// 搜索功能组合
export function Search(){
    return (
    <div>  
        <SearchBg/>
        <SearchBox/>
        <SearchMode/>
        <SearchTips/>
    </div>
    )
}
