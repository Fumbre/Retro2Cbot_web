import { wsNeopixelsData } from '@partials/robot/Neopixels/neopixels';
import './robots.sass'
import { createReflectiveGraphic, wsReflectiveData } from '@partials/robot/Reflective/reflective';

export async function createDOMRobots() {
  try {
    const reflectiveSensorEl = document.querySelectorAll(".reflective_sensor[data-robot-code]")

    reflectiveSensorEl.forEach((currentEl) => {
      const { robotCode, robotName } = currentEl.dataset;

      createReflectiveGraphic(currentEl, robotName, robotCode)
    })


    wsReflectiveData();
    wsNeopixelsData();
  } catch (e) {
    console.log(e)
  }
  // to do instead of fetch use data-endpoint
  // try {
  //   const robotsRes = await (await fetch(`/api/robots`)).json();
  //   if (robotsRes.code != 200) {
  //     throw new Error("can't catch robots database");
  //   }

  //   const robotsData = robotsRes.data;

  //   // await Promise.all(
  //   // robotsData.map(robot => loadReflective(robot))
  //   // )

  //   for (const robot of robotsData) {
  //     // console.log(iterator)
  //     requestAnimationFrame(() => {
  //       createReflectiveGraphic(robot.robotName, robot.robotCode);
  //     })
  //   }




  // } catch (e) {
  //   return e
  // }

}

async function loadReflective(robot) {
  const idElement = document.getElementById(`robots__status_${robot.robotCode}`);

  const rsElement = await (await fetch(`/robot/${robot.robotCode}/sensors/reflective?partials=true`)).text()
  idElement.innerHTML = rsElement;


  createReflectiveGraphic(robot.robotName, robot.robotCode);
  // requestAnimationFrame(async () => {
  // })

}