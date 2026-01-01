import './reflective.sass'
import { ws } from '../../../../assets/scripts/main.js';
import { ROBOTS, isRobot } from '../../../../assets/scripts/constants.js';
import wsBus from '../../../../assets/scripts/wsBus.js';

import * as echarts from 'echarts';
const charts = new Map();

let currentRobot;

function getSeriesColor(i) {
    return getComputedStyle(document.documentElement)
        .getPropertyValue(`--rs-a${i}`)
        .trim();
}

export function getReflectiveData() {
    // if (!isRobot(robotId))
    //     return;

    console.log('reflect?')

    if (ws.readyState === WebSocket.OPEN) {
        wsBus.on('rs', (data) => {
            const dataParsed = JSON.parse(data)
            console.log("ws bus got rs data", dataParsed)
            updateReflectiveSensors(dataParsed.data);
        })
        // ws.send(JSON.stringify({
        //     event: "rs",
        //     method: "GET",
        //     robotCode: robotId
        // }));
    }

    // ws.send(JSON.stringify({ test: "test" }))
}


export function createGraphic(robotCode) {
    const rsList = document.getElementById(`rsList__${robotCode}`);

    const rsId = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7'];

    const graphEl = rsList.parentElement.querySelector(".reflective_sensor__graph");


    var myChart = echarts.init(graphEl);
    var option;

    option = {
        title: {
            text: 'Reflective data',
            subtext: `${robotCode}`
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            show: false,
            // data: rsId
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false
        },
        yAxis: {
            type: 'value'
        },
        series: rsId.map((id, i) => ({
            name: id,
            type: 'line',
            data: [234 * i, 234, 124, 994, 223 * i, 253, 252], // use fetch api in node js for createatin first data
            lineStyle: {
                color: getSeriesColor(i),
            },
            itemStyle: {
                color: getSeriesColor(i),
            },
        }))
    };


    option && myChart.setOption(option);

    const activeSeries = new Set(
        myChart.getOption().series.map(s => s.name)
    );

    document.getElementById(`rsList__${robotCode}`).addEventListener('click', (e) => {
        const li = e.target.closest(`[data-series]`);

        if (!li) return;

        const seriesName = li.dataset.series;
        console.log(li.dataset)
        console.log(li.dataset.series)

        const isActive = activeSeries.has(seriesName);

        myChart.dispatchAction({
            type: isActive ? 'legendUnSelect' : 'legendSelect',
            name: seriesName,
        });

        if (isActive) {
            activeSeries.delete(seriesName);
            li.classList.add('disabled');
        } else {
            activeSeries.add(seriesName);
            li.classList.remove('disabled');
        }
    });
}

// todo updateGraphic


// used every time when recieved data from socket
function updateReflectiveSensors(data) {
    const rsData = data[0];
    const rsList = document.getElementById(`rsList__${rsData.robotCode}`);

    // console.log(rsList);

    for (let index = 0; index < rsList.childElementCount; index++) {
        const item = rsList.querySelector(`[data-sensor="reflective_sensor__a${index}"]`)
        const valueEl = item.querySelector('.reflective_sensor__value');

        valueEl.textContent = rsData[`a${index}`];

        valueEl.classList.remove('reflective_sensor__line_status0');
        valueEl.classList.remove('reflective_sensor__line_status1');
        valueEl.classList.add(`reflective_sensor__line_status${rsData.currentStatus.slice(index, index + 1)}`);

        console.log(item);

    }



}