export const ROBOTS = Object.freeze({
  BB016: "BB016",
  BB011: "BB011",
  BB046: "BB046",
});

export function isRobot(robotId) {
  let isRobot = false;
  for (const robot in ROBOTS) {
    if (robot === robotId) {
      isRobot = true;
    }
  }
  if (!isRobot) {
    console.log('no such robot');
  }
  return isRobot;
}