import "../style/normalize.scss";
import "../style/global.sass";
import "../style/header.sass";
import "../style/main.sass";
import { nodeWebsocket } from "@websocket/websocket"
import { createReflectiveGraphic, wsReflectiveData } from "@partials/robot/Reflective/reflective";

// TODO:
// import "../style/footer.sass";

// create node websocket
nodeWebsocket();

const page = document.body.dataset.page;

// use new script for /robots
if (page === 'robots' || page === 'reflective') {
  try {
    const { createDOMRobots } = await import("@pages/Robots/robots");
    await createDOMRobots();
  } catch (e) {
    console.log(e)
  }
}
