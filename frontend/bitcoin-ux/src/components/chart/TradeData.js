import React, {useState, useEffect} from 'react'
import {API_URL, TRADE_DATA} from '../../constance/index'
import Axios from 'axios'
//import Table from 'react-bootstrap/Table'
import Calculations from './Calculations'
import TableContainer from '@material-ui/core/TableContainer';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import { Container } from '@material-ui/core';
import useWindowDimensions from '../window/Window'




function timeStampToDate(time){
    const temp = new Date(time)
    const ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(temp)
    const mo = new Intl.DateTimeFormat('en', { month: '2-digit' }).format(temp)
    const da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(temp)
    const hr = new Intl.DateTimeFormat('en-US', { hour: 'numeric' }).format(temp)
    return ye+'-'+mo+'-'+da+' - '+hr
}


function TradeData(props){
    const { height, width } = useWindowDimensions();
    const [tradeData, setTradeData] = useState({ count: 0, next: '', previous:'', trades:[{decision: '', closePrice: '', closeTime: ''}]})
    const [page, setPage] = useState(0)
    const [rowsPerPage, setRowsPerPage] = useState(10)
    const end_url = '?coinData__pair='+props.pair+'&limit=100'

    const handleChangePage = (event, newPage) => {
        setPage(newPage)
    }

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value)
        setPage(0)
    }

    useEffect(() => {
        Axios.get(API_URL+TRADE_DATA+end_url)
        .then(res => {
            const count = res.data.count
            const nextLink = res.data.next
            const prevLink = res.data.previous
            const trade = res.data.results
            setTradeData({
                count: count,
                next: nextLink,
                previous: prevLink,
                trades:
                trade.map(each => ({
                    decision: (each.decision === 1) ? 'Buy' : 'Sell',
                    closePrice: Number(each.coinData.closePrice),
                    closeTime: (width < 500) ? timeStampToDate(each.coinData.closeTime).slice(5) : timeStampToDate(each.coinData.closeTime),
                }))
            })
        })
        .catch(error => {
            console.log(error)
        })
    }, [end_url, width])

    return (
        <Container maxWidth= 'md'>
            <TableContainer style={{maxHeight: (height > 900) ? height/1.6 : (height > 700 ) ? height/1.8 : height/2}}>
                <Table size= {width >  1000 ? "medium" : "small"} stickyHeader aria-label="sticky table">
                    <TableHead>
                        <TableRow>
                            <TableCell
                                key={'decision'}
                                align={'left'}
                                >Decision</TableCell>
                            <TableCell
                                key={'price'}
                                align={'left'}
                                >Price</TableCell>
                            <TableCell
                                key={'time'}
                                align={'left'}
                                >Time</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {tradeData.trades.slice(page * rowsPerPage, page*rowsPerPage + rowsPerPage).map(trade => (
                            <TableRow hover key={trade.closeTime}  tabIndex={-1} align={'left'}>
                            <TableCell align={'left'}> {trade.decision} </TableCell>
                            <TableCell align={'left'}> {trade.closePrice} </TableCell>
                            <TableCell align={'left'}> {trade.closeTime} </TableCell> 
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <br></br>
            <TablePagination
                rowsPerPageOptions={[10, 25, 50, 100]}
                component="div"
                count={tradeData.trades.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onChangePage={handleChangePage}
                onChangeRowsPerPage={handleChangeRowsPerPage}
            />
            <br></br>
            <Calculations trades={tradeData.trades.slice(page * rowsPerPage, page*rowsPerPage + rowsPerPage)}/>
        </Container>
    )
}

export default TradeData