import { Show,createSignal } from "solid-js";
import "./assets/css/style.css"

export function AWCanvas(props){
    const def_class_name = "aw_border"

    return (
        <div
            className={ def_class_name + (props.className == undefined ? "" : " " + props.className)}
            onClick={props.onClick}
        >
            {props.content}
            {props.children}
        </div>
    )
}

export function AWText(props){
    const def_class_name = "aw_border input_dom"
    const box_def_class_name = "input_box"
    return (
        <div
            className={ box_def_class_name + (props.boxClassName == undefined ? "" : " " + props.boxClassName)}
        >
            <Show when={props.label != undefined} fallback={""}>
                <AWLabel label = {props.label} />
            </Show>
            <input 
                ref = {props.ref}
                className={ def_class_name + (props.className == undefined ? "" : " " + props.className)}
                tabindex="0" 
                contenteditable="true"
                onInput={props.onInput}
                onClick={props.onClick}
                onBlur={props.onBlur}
                type="text"
            />
        </div>
    )
}

export function AWPasswd(props){
    const def_class_name = "aw_border input_dom pw"
    const box_def_class_name = "input_box"
    return (
        <div
            className={ box_def_class_name + (props.boxClassName == undefined ? "" : " " + props.boxClassName)}
        >
            <Show when={props.label != undefined} fallback={""}>
                <AWLabel label = {props.label} />
            </Show>
            <input 
                ref = {props.ref}
                className={ def_class_name + (props.className == undefined ? "" : " " + props.className)}
                tabindex="0" 
                contenteditable="true"
                onInput={props.onInput}
                onClick={props.onClick}
                onBlur={props.onBlur}
                type="password"
            />
        </div>
    )
}

export function AWLabel(props){
    const def_class_name = "label"

    return (
        <div 
            className={ def_class_name + (props.className == undefined ? "" : " " + props.className)}
            onClick={props.onClick}
        >
            {props.label}
        </div>
    )
}

export function AWTips(props){
    const def_class_name = "tips"

    return (
    <div 
        className= { def_class_name + (props.className == undefined ? "" : " " + props.className)}
        onClick={props.onClick}
    >
        {props.content}
    </div>
    )
}

export function AWMsg(type,content,head=undefined,time=2000){
    /* 初始参数 */
    const type_list = ["success","warning","msg","error"] 
    const type_list_color = {
        "success": "rgb(0, 209, 73)",
        "warning": "rgb(209, 209, 4)",
        "error": "rgb(209, 0, 0)",
        "msg":"rgb(61, 152, 209)"
    }
    const [top,setTop] = createSignal(-40)

    if( type_list.indexOf(type) == -1 ){
        throw "非规定标签类型"
    }

     // 消息盒子
    let aw_msg_box
    let msg_box = (
        <div 
            className= "msg_box"
            id = "msg_box"
            style = {{
                top: top()+"px"
            }}
            ref = {aw_msg_box}
        >
            <div 
                className="msg aw_border"
                style={{
                    "border-color": type_list_color[type],
                    color: type_list_color[type],
                }}
            >
                <div>{head == undefined?type:head}:</div>
                <div>{content}</div>
            </div>
        </div>
    )

    /* 初始参数 end */

     // 核心流程
    msgBoxCore()

     // 判断是否存在msg_box消息盒子
    function msgBoxCore(){
        document.body.appendChild(msg_box)
        setTimeout(()=>{
            setTop(()=>12)
        },200)
        setTimeout(()=>{
            document.body.removeChild(msg_box)
        }, 200+time)
    }
}