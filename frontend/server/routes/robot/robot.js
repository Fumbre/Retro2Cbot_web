import dotenv from 'dotenv';
dotenv.config();
import express from "express"
import { validateRobot } from '../../middleware/validateRobot.js';
import { getRobots } from '../../api/robots.js';

const router = express.Router();


router.get('/robots', async (req, res) => {
    console.log(process.env.API_IP)
    try {
        const robots = await getRobots();

        return res.render('./Robots/robots', {
            title: "about robots",
            data: robots.data
        })
    } catch (e) {
        console.error(e);
    }

    // return res.json(robots)

})

router.get('/robot/:id', validateRobot, async (req, res) => {
    try {
        // let robots = await (await fetch(`http://${process.env.API_IP}:${process.env.API_PORT}/robots`)).json();

        // const currentRobot = robots.data.filter((item) => item.robotCode.toLowerCase() == req.robotCode.toLowerCase())[0]
        // console.log(currentRobot)
        // return res.render('Robot/robot', {
        //     title: `${currentRobot.robotName} (${currentRobot.robotCode})`,
        // })

        return res.redirect('/')
    } catch (e) {
        console.error(e);
        return res.redirect('/')
    }

})

export { router };