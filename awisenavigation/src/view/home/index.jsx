import { Search } from "./assembly/search/index";
import Background from "./assembly/background/index";
import Fast from "./assembly/fastlist/index";

function Home(){
    return (
    <div id = "home">
        <Background/>
        <Search/>
        <Fast/>
    </div>)
}
export default Home