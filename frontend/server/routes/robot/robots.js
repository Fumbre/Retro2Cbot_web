import dotenv from 'dotenv';
dotenv.config();
import express from "express"
// import { validateRobot } from '../../middleware/validateRobot.js';
import { getRobots, getLastRSData, getLastNeopixelsData, getLastSonarData } from '../../api/robots.js';

const router = express.Router();


router.get('/robots', async (req, res) => {
    // console.log(process.env.API_IP)
    try {
        const robots = await getRobots();


        await Promise.all(
            robots.data.map(async (robot) => {

                robot.sensorsReflective = [];
                robot.sensorsNeopixels = [];
                robot.sensorsSonar = [];

                const [
                    rsLastData,
                    neopixelsLastData,
                    sonarLastData
                ] = await Promise.all([
                    getLastRSData(robot.robotCode),
                    getLastNeopixelsData(robot.robotCode),
                    getLastSonarData(robot.robotCode),
                ]);

                for (let index = 0; index < 8; index++) {
                    const element = rsLastData[`a${index}`] || 0;
                    robot.sensorsReflective.push(element)
                }
                robot.reflectiveStatus = rsLastData.currentStatus || '00000000';

                // add data to neopixel if not exist
                for (let i = 0; i < 4; i++) {
                    if (!neopixelsLastData[i]) {
                        neopixelsLastData[i] = {
                            neopixelIndex: i,
                            r: 0,
                            g: 0,
                            b: 0,
                        }
                    }
                }

                robot.sensorsNeopixels.push(...neopixelsLastData);


                if (robot.robotCode === "BB011") {
                    robot.sensorsSonar.push(...sonarLastData);
                } else {
                    sonarLastData.length != 0 ?
                        robot.sensorsSonar.push(...sonarLastData) : robot.sensorsSonar.push(
                            {
                                direction: '0',
                                sonarDistance: 0,
                            }
                        )
                }

            })
        );


        // for (let index = 0; index < robots.data.length; index++) {
        //     const item = robots.data[index];
        //     console.log(item);
        //     const rs = await getRSData()
        // }


        return res.render('./pages/Robots/robots', {
            title: "about robots",
            page: "robots",
            data: robots.data,
        })
    } catch (e) {
        console.error(e);
    }
})

// router.get('/robot/:id', validateRobot, async (req, res) => {
//     try {
//         // let robots = await (await fetch(`http://${process.env.API_IP}:${process.env.API_PORT}/robots`)).json();

//         // const currentRobot = robots.data.filter((item) => item.robotCode.toLowerCase() == req.robotCode.toLowerCase())[0]
//         // console.log(currentRobot)
//         // return res.render('Robot/robot', {
//         //     title: `${currentRobot.robotName} (${currentRobot.robotCode})`,
//         // })

//         return res.redirect('/')
//     } catch (e) {
//         console.error(e);
//         return res.redirect('/')
//     }

// })

export { router };