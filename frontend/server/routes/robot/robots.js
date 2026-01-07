import dotenv from 'dotenv';
dotenv.config();
import express from "express"
// import { validateRobot } from '../../middleware/validateRobot.js';
import { getRobots, getLastRSData } from '../../api/robots.js';

const router = express.Router();


router.get('/robots', async (req, res) => {
    // console.log(process.env.API_IP)
    try {
        const robots = await getRobots();


        await Promise.all(
            robots.data.map(async (robot) => {
                robot.sensorsReflective = [];
                const data = await getLastRSData(robot.robotCode);
                // console.log('aaaaaaaaaaaaaaaaaaa: ', data);
                for (let index = 0; index < 8; index++) {
                    const element = data[`a${index}`] || 0;
                    robot.sensorsReflective.push(element)
                }
                robot.reflectiveStatus = data.currentStatus || '00000000';

            })
        );

        console.log(robots.data);

        // for (let index = 0; index < robots.data.length; index++) {
        //     const item = robots.data[index];
        //     console.log(item);
        //     const rs = await getRSData()
        // }


        return res.render('./pages/Robots/robots', {
            title: "about robots",
            page: "robots",
            data: robots.data,
            sensors: [203, 21, 234, 23, 239, 124, 234, 23],
            currentStatus: '10011110'
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