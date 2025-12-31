import { el, mount } from "redom";
import "../style/normalize.scss";
import "../style/global.sass";
import "../style/header.sass";
import "../style/main.sass";
import { getReflectiveData } from "../../views/Robot/Sensors/Reflective/reflective.js"
import { nodeWebsocket } from "./websocket.js"
import { getStatus } from "../../views/Robot/robot.js";

// TODO:
// import "../style/footer.sass";

// async function getRobot() {
//   const robots = await fetch('/robot');
//   console.log(await robots.json());
// }

export const ws = nodeWebsocket();

await getStatus();

getReflectiveData();

// await getRobot();

