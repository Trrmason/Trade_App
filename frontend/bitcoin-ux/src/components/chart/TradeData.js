import React, {useState, useEffect} from 'react'
import {API_URL, TRADE_DATA} from '../../constance/index'
import Axios from 'axios'
import Table from 'react-bootstrap/Table'


function timeStampToDate(time){
    const temp = new Date(time)
    const ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(temp)
    const mo = new Intl.DateTimeFormat('en', { month: '2-digit' }).format(temp)
    const da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(temp)
    const hr = new Intl.DateTimeFormat('en-US', { hour: 'numeric' }).format(temp)
    return ye+'-'+mo+'-'+da+' - '+hr
}

function TradeData(props){
    const [tradeData, setTradeData] = useState([{decision: '', closePrice: '', closeTime: ''}])
    //Set round amount for display
    useEffect(() => {
        Axios.get(API_URL+TRADE_DATA+'?coinData__pair='+props.pair)
        .then(res => {
            const trade = res.data.results
            setTradeData(trade.map(each => ({
                decision: (each.decision === 1) ? 'Buy' : 'Sell',
                closePrice: Number(each.coinData.closePrice),
                closeTime: timeStampToDate(each.coinData.closeTime)
            })))
        })
        .catch(error => {
            console.log(error)
        })
    }, [props])
    return (
        <div className='tradeTable'>
            <Table striped hover responsive varient='dark'>
                <thead>
                    <tr>
                        <th>Decision</th>
                        <th>Price</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {tradeData.map(trade => (
                        <tr key={trade.closeTime}>
                        <td> {trade.decision} </td>
                        <td> {trade.closePrice} </td>
                        <td> {trade.closeTime} </td> 
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    )
}

export default TradeData