import dotenv from 'dotenv';
dotenv.config();
import express from "express"
import { validateRobot } from '../../middleware/validateRobot.js';

const router = express.Router();


router.get('/robot', async (req, res) => {
    console.log(process.env.API_IP)
    try {
        const robots = await (await fetch(`http://${process.env.API_IP}:${process.env.API_PORT}/robots`)).json();

        if (robots.code != 200) {
            throw new Error('code is not 200')
        }

        return res.render('./Robot/robot', {
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
        let robots = await (await fetch(`http://${process.env.API_IP}:${process.env.API_PORT}/robots`)).json();

        const currentRobot = robots.data.filter((item) => item.robotCode.toLowerCase() == req.robotCode.toLowerCase())[0]
        console.log(currentRobot)
        return res.json(currentRobot)
    } catch (e) {
        console.error(e);
        return res.redirect('/')
    }

})

export { router };