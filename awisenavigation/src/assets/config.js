export const config = {
    "search": {
        "web": [
            {
                "name":"bing",
                "method":"get",
                "url":"https://cn.bing.com/search",
                "keys":["q"],
                "icon":"/src/assets/img/icon/bing.png",
                "getid":true                
            },
            {
                "name": "baidu",
                "method": "get",
                "url": "https://www.baidu.com/baidu",
                "keys": ["word"],
                "icon": "/src/assets/img/icon/baidu.png",
                "getid":true
            },
            {
                "name": "少年梦阅读",
                "method": "get",
                "url": "https://www.shaoniandream.com/library/str/0_0_0_0_0_0_0_1_",
                "keys":[],
                "icon": "/src/assets/img/icon/shaoniandream.png",
                "getid":false
            },
            {
                "name": "bilibili",
                "method": "get",
                "url": "https://search.bilibili.com/all",
                "keys": ["keyword"],
                "icon": "/src/assets/img/icon/bilibili.png",
                "getid":true
            },
            {
                "name": "google",
                "method": "get",
                "url": "https://www.google.com/search?",
                "keys": ["q"],
                "icon": "/src/assets/img/icon/google.png",
                "getid":true
            }
        ]
    },
    "fastlist": [
        /*           url               images         title          */
        ["https://www.pixiv.net/", "/src/assets/img/pz.jpg", "pixiv"],
        ["https://www.dmzj.com/", "/src/assets/img/dmzj.png", "动漫之家"],
        ["http://upupoo.com/", "/src/assets/img/upup.png", "upupoo"],
        ["https://music.163.com/", "/src/assets/img/wyy.png", "网易云音乐"],
        ["https://store.steampowered.com/", "/src/assets/img/steam.jpg", "steam"],
        ["http://www.bilibili.com/", "/src/assets/img/bz.png", "bilibili"],
        ["https://www.shaoniandream.com/", "/src/assets/img/snm.png", "少年梦"],
        ["https://rpg.blue/forum.php", "/src/assets/img/project1.jpg", "project1"],
        ["https://yidaimingjvn.xyz", "/src/assets/img/tx.jpg", "一代明君的小屋"],
        ["https://www.isekai.cn", "/src/assets/img/ysjbk.png", "异世界百科"],
        ["https://www.8kana.com/", "/src/assets/img/8z.jpg", "不可能的世界"]
    ]
}