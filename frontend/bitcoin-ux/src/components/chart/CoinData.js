import React, {useState, useEffect} from 'react'
import {API_URL, COIN_DATA} from '../../constance/index'
import Axios from 'axios'
import Chart from "react-apexcharts"
import useWindowDimensions from '../window/Window'


function timeStampToDate(time){
    const temp = new Date(time)
    const ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(temp)
    const mo = new Intl.DateTimeFormat('en', { month: '2-digit' }).format(temp)
    const da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(temp)
    const hr = new Intl.DateTimeFormat('en-US', { hour: 'numeric' }).format(temp)
    return ye+'-'+mo+'-'+da+' - '+hr
}

const chartResponsive = (width, height) => {
    let widthOut = width/1.5
    let heightOut = height/1.25
    widthOut = (width < 1000) ? '100%' : width/1.6
    return {widthOut, heightOut}
}
function CoinData(props){
    const [coinData, setCoinData] = useState([])
    const { height, width } = useWindowDimensions();
    //Set round amount for display
    useEffect(() => {
        const limitAmount =  (width > 1000) ? '120' : '30'
        Axios.get(API_URL+COIN_DATA+'?pair='+props.pair+'&limit='+limitAmount)
        .then(res => {
            const prices = res.data.results
            setCoinData(prices.reverse())
        })
        .catch(error => {
            console.log(error)
        })
    }, [props, width])

    const dohlc = coinData.map(price => ({
        x: timeStampToDate(price.openTime).toString(),
        y: [
            Number(price.openPrice), 
            Number(price.highPrice), 
            Number(price.lowPrice), 
            Number(price.closePrice)
        ]
    }),)
    
    const currentPrice = (coinData.length === 0) ? '' : Number(coinData[coinData.length - 1].closePrice)

    useEffect(() => {
        document.title = props.pair + ' - ' + currentPrice
    })

    //
    //Chart Config
    const chartConfig = {
        series:[{
            data: dohlc
            }],
        options: {
            chart: {
                id: "candlestick",
                background: 'white',
                defaultLocale: 'en',
                toolbar: {
                    show: true,
                    offsetX: 0,
                    offsetY: 0,
                    tools: {
                      download: false,
                      selection: true,
                      zoom: true,
                      zoomin: false,
                      zoomout: false,
                      pan: false,
                      reset: true | '<img src="/static/icons/reset.png" width="20">',
                      customIcons: []
                    },
                    autoSelected: 'zoom' 
                  },
                  animations: {
                    enabled: true,
                    easing: 'easeinout',
                    speed: 800,
                    animateGradually: {
                        enabled: true,
                        delay: 150
                    },
                    dynamicAnimation: {
                        enabled: true,
                        speed: 350
                    }
                },
            },
            grid: {
                show: true,
                borderColor: '#ECECEC',
                strokeDashArray: 0,
                position: 'back',
                xaxis: {
                    lines: {
                        show: false
                    }
                },   
                yaxis: {
                    lines: {
                        show: true
                    }
                },  
            },
            plotOptions: {
                candlestick: {
                  colors: {
                    upward: '#BEF7C9',
                    downward: '#FF9B9B'
                  },
                  wick: {
                    useFillColor: false
                  }
                }
            },
            title: {
                text: props.pair + ' - ' + currentPrice,
                align: 'center',
                margin: 10,
                offsetX: 0,
                offsetY: 0,
                floating: false,
                style: {
                  fontSize:  '20px',
                  fontWeight:  'strong',
                  fontFamily:  undefined,
                  color:  '#343A40'
                },
            },
            xaxis: {
                type: 'category',
                categories: [],
                labels: {
                    show: false,
                    rotate: -45,
                    rotateAlways: false,
                    hideOverlappingLabels: true,
                    showDuplicates: false,
                    trim: true,
                    minHeight: undefined,
                    maxHeight: 200,
                    style: {
                        colors: [],
                        fontSize: '12px',
                        fontFamily: 'Helvetica, Arial, sans-serif',
                        fontWeight: 100,
                        cssClass: 'apexcharts-xaxis-label',
                    },
                    offsetX: 0,
                    offsetY: 0,
                    format: undefined,
                    formatter: undefined,
                    datetimeUTC: true,
                    datetimeFormatter: {
                        year: 'yyyy',
                        month: "MMM 'yy",
                        day: 'dd MMM',
                        hour: 'HH:mm',
                    },
                },
            }
        }
    }
    //Chart Config
    //
    const dimensions = chartResponsive(width, height)
    return(
        <div>
            <Chart
            options={chartConfig.options}
            series={chartConfig.series}
            type="candlestick"
            width= {dimensions.widthOut}
            height = {dimensions.heightOut}
            />
        </div>
    )

}



export default CoinData
