import { el, mount } from "redom";
import "../style/normalize.scss";
import "../style/global.sass";
import "../style/header.sass";
import "../style/main.sass";
import { nodeWebsocket } from "./websocket.js"
import { createDOMRobots } from "../../views/Robots/robots.js";

// TODO:
// import "../style/footer.sass";

export const ws = nodeWebsocket();

// use new script for /robot
await createDOMRobots();




// await getRobot();

