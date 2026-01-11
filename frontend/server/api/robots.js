import express from 'express';
import { validateRobot } from '../middleware/validateRobot.js';
const router = express.Router();

router.get('/robots', async (req, res) => {
  const data = await getRobots()
  console.log('this is from api/robots node', data);
  return res.json(data);
});

router.get('/robots/:id/rs', validateRobot, async (req, res) => {
  const data = await getRSData(req.params["id"])
  return res.json(data);
})


async function getRobots() {
  try {
    const robots = await (await fetch(`${process.env.API_PROTOCOL}://${process.env.API_URL}/robots`)).json();

    if (robots.code != 200) {
      console.error('Get robots code is not 200')
      return robots
    }

    return robots;
  } catch (e) {
    return e
  }
}


async function getRSData(robotCode) {
  try {
    const robotSensor = await (await fetch(`${process.env.API_PROTOCOL}://${process.env.API_URL}/robots/${robotCode}/rs`)).json();

    if (robotSensor.code != 200) {
      console.error('Get robotSensor code is not 200')
      return robotSensor
    }

    return robotSensor.data;
  } catch (e) {
    return e
  }
}

async function getLastRSData(robotCode) {
  try {
    const robotSensor = await (await fetch(`${process.env.API_PROTOCOL}://${process.env.API_URL}/robots/newdata/${robotCode}/rs`)).json();

    if (robotSensor.code != 200) {
      console.error('Get robotSensor code is not 200 in getLastRSData')
      throw new Error("robotSensor code is not 200 in getLastRSData");
    }

    return robotSensor.data;
  } catch (e) {
    return [];
  }
}

export { router, getRobots, getRSData, getLastRSData };
