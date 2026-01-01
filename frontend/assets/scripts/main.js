import { el, mount } from "redom";
import "../style/normalize.scss";
import "../style/global.sass";
import "../style/header.sass";
import "../style/main.sass";
import { getReflectiveData, updateGraphic } from "../../views/Robot/Sensors/Reflective/reflective.js"
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

// use new script for /robot
// when fetch robots create graphics
createGraphic('BB016');
createGraphic('BB046');
createGraphic('BB011');

// await getRobot();

