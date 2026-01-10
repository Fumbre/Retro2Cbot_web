import './reflective.sass'
import wsBus from '@websocket/wsBus';

import * as echarts from 'echarts';
const charts = new Map();
const buffers = {};

const MAX_CHAR_DATA = 30;
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


export async function createReflectiveGraphic(root, robotName, robotCode) {
    const rsData = await (await fetch(`api/robots/${robotCode}/rs`)).json();

    // to do cut data somehow and put it to graphic
    console.log(rsData);
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
        series: rsId.map((id, i) => {
            buffers[id] = [234 * i, 234, 124, 994, 223 * i, 253, 252];

            return ({
                name: id,
                type: 'line',
                data: buffers[id], // use fetch api in node js for createatin first data
                lineStyle: {
                    color: getSeriesColor(i),
                },
                itemStyle: {
                    color: getSeriesColor(i),
                },
            })
        }
        )
    };


    myChart.setOption(option);


    const activeSeries = new Set(rsId); // to get id's for series 

    charts.set(robotCode, {
        chart: myChart,
        buffers,
        activeSeries
    });

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

    const entry = charts.get(rsData.robotCode);
    if (!entry) return;

    const { chart, buffers } = entry;

    for (const key in buffers) {
        buffers[key].push(rsData[key]);
        if (buffers[key].length > MAX_CHAR_DATA) {
            buffers[key].shift();
        }
    }

    chart.setOption({
        series: Object.entries(buffers).map(([key, arr]) => ({
            name: key,
            data: arr
        }))
    });
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