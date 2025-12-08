import { el, mount } from "redom";
import "../style/normalize.scss";
import "../style/global.sass";
import "../style/main.sass";

const app = el("div", { class: "app" }, "Hello from ReDOM!");
mount(document.body, app);

console.log("test");
