import './reflective.sass'
import wsBus from '@websocket/wsBus';

import * as echarts from 'echarts';
const charts = new Map();

let reflectiveSubscribed = false;

function getSeriesColor(i) {
    return getComputedStyle(document.documentElement)
        .getPropertyValue(`--rs-a${i}`)
        .trim();
}

export function wsReflectiveData() {
    // subscribe only once
    if (reflectiveSubscribed) return;
    reflectiveSubscribed = true;

    wsBus.on('rs', (data) => {
        const dataParsed = JSON.parse(data);
        console.log("ws bus got rs data", dataParsed);
        updateReflectiveSensors(dataParsed.data);
        updateGraphic(dataParsed.data);
    });
}


export function createReflectiveGraphic(root, robotName, robotCode) {
    const rsId = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7'];

    const graphEl = root.parentElement.querySelector(".reflective_sensor__graph");


    var myChart = echarts.init(graphEl);
    var option;

    option = {
        title: {
            text: 'Reflective data',
            subtext: `${robotName} (${robotCode})`
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

    charts.set(robotCode, activeSeries);

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
function updateGraphic(data) {
    const rsData = data[0];
    const rsElement = document.querySelector(`.reflective_sensor[data-robot-code=${rsData.robotCode}]`);
    const rsGraphEl = rsElement.querySelector('.reflective_sensor__graph');
    console.log(rsGraphEl)
}


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
    }

}