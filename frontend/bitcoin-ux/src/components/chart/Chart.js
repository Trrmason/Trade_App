import React, {useState, useEffect} from 'react'
import CoinData from './CoinData'
import TradeData from './TradeData'
import 'bootstrap/dist/css/bootstrap.css';
import Dropdown from 'react-bootstrap/Dropdown';


function Chart() {
    let initState = ''

    const [pair, setPair] = useState(initState)

    useEffect(() =>{
        const data = localStorage.getItem('pair')
        if (data){
            setPair(data)
        }
        else{
            setPair('BTCUSDT')
        }
    },[])

    useEffect(() =>{
        localStorage.setItem('pair', pair)
    })

    if (pair === ''){
        return <div></div>
    }

    return (
        <div className='container-fluid'>
            <div className='Chart'>
                <CoinData pair={pair} />
            </div>
            <div>
                <TradeData pair={pair} />
            </div>
            <div>
                <Dropdown className='dropdown'>
                    <Dropdown.Toggle id="dropdown-basic-button" variant='secondary' key='Info' className='dropdownCustom'>
                        Trade Pairs
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                        <Dropdown.Item id='BTCUSDT' onClick={(e) => setPair(e.target.id)}>BTCUSDT</Dropdown.Item>
                        <Dropdown.Item id='ETHBTC' onClick={(e) => setPair(e.target.id)}>ETHBTC</Dropdown.Item>
                        <Dropdown.Item id='XRPBTC' onClick={(e) => setPair(e.target.id)}>XRPBTC</Dropdown.Item>
                        <Dropdown.Item id='TRXBTC' onClick={(e) => setPair(e.target.id)}>TRXBTC</Dropdown.Item>
                        <Dropdown.Item id='LINKBTC' onClick={(e) => setPair(e.target.id)}>LINKBTC</Dropdown.Item>
                        <Dropdown.Item id='BATBTC' onClick={(e) => setPair(e.target.id)}>BATBTC</Dropdown.Item>
                    </Dropdown.Menu>
                </Dropdown>
            </div>
        </div>
    )
}

export default Chart