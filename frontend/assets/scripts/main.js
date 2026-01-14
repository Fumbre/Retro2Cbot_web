import "../style/normalize.scss";
import "../style/global.sass";
import "../style/header.sass";
import "../style/main.sass";

import group_front_page from '../img/group_front_page.jpg'
import member_1 from '../img/members/member_1.jpg'
import mem2 from '../img/members/member_2.jpg'
import mem3 from '../img/members/member_3.jpg'
import mem4 from '../img/members/member_4.jpg'

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
