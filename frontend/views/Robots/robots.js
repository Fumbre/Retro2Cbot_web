import './robots.sass'
import { createReflectiveGraphic, wsReflectiveData } from './Sensors/Reflective/reflective.js';

export async function createDOMRobots() {
  try {
    const robotsRes = await (await fetch(`/api/robots`)).json();
    if (robotsRes.code != 200) {
      throw new Error("can't catch robots database");
    }

    const robotsData = robotsRes.data;

    await Promise.all(
      robotsData.map(robot => loadReflective(robot.robotCode))
    )

    wsReflectiveData();

  } catch (e) {
    return e
  }

}

async function loadReflective(robotCode) {
  const idElement = document.getElementById(`robots__status_${robotCode}`);

  const rsElement = await (await fetch(`/robot/${robotCode}/sensors/reflective?html=true`)).text()
  idElement.innerHTML = rsElement;

  createReflectiveGraphic(robotCode);
}