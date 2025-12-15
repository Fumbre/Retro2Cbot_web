import dotenv from 'dotenv';
dotenv.config();
import express from "express"

const router = express.Router();


router.get('/robot', async (req, res) => {
    console.log(process.env.API_IP)
    const robots = await (await fetch(`http://${process.env.API_IP}:${process.env.API_PORT}/robots`)).json();
    console.log(robots);
    return res.json(robots)
})

router.get('/robot/status/:id', async (req, res) => {
    try {
        let robots = await (await fetch(`http://${process.env.API_IP}:${process.env.API_PORT}/robots`)).json();

        const test = robots.data.filter((item) => item.robotCode.toLowerCase() == req.params.id.toLowerCase())[0]
        console.log(test)
        return res.json(test)
    } catch (e) {
        return res.redirect('/')
    }

})

export { router };