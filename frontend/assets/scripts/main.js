import { el, mount } from "redom";
import "../style/normalize.scss";
import "../style/global.sass";
import "../style/header.sass";
import "../style/main.sass";

// const app = el("div", { class: "app" }, "Hello robot");
// mount(document.body, app);

async function getRobot() {
  const robots = await fetch('/robot');
  console.log(await robots.json());
}

await getRobot();