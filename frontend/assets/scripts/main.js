import { el, mount } from "redom";
import "../style/normalize.scss";
import "../style/global.sass";
import "../style/header.sass";
import "../style/main.sass";
import { test } from "../../views/Robot/Sensors/Reflective/reflective.js"


// TODO:
// import "../style/footer.sass";

async function getRobot() {
  const robots = await fetch('/robot');
  console.log(await robots.json());
}

await getRobot();

test();