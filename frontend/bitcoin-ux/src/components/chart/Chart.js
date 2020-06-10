import React, {useState, useEffect} from 'react'
import CoinData from './CoinData'
import TradeData from './TradeData'
import 'bootstrap/dist/css/bootstrap.css'
import Paper from '@material-ui/core/Paper'
import { makeStyles } from '@material-ui/core/styles'
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import Menu from '@material-ui/core/Menu';




const useStyles = makeStyles(
    {
    root: {
      width: '100%',
      height: '100%'
    },
    title: {
        flexGrow: 1,
      },
 });


function Chart() {
    let initState = ''
    const classes = useStyles();
    const [pair, setPair] = useState(initState)
    const [anchorEl, setAnchorEl] = useState(null)
    // eslint-disable-next-line
    const [time, setTime] = useState(Date.now())
    const open = Boolean(anchorEl);
    useEffect(() => {
        const interval = setInterval(() => setTime(Date.now()), 300000)
        return () => {
            clearInterval(interval)
        }
    }, [])

    useEffect(() =>{
        const data = localStorage.getItem('pair')
        if (data){
            setPair(data)
        }
        else{
            setPair('BTCUSDT')
        }
    },[])

    useEffect(() => {
        localStorage.setItem('pair', pair)
    })

    const handleClick = (e) => {
        setAnchorEl(e.currentTarget)
    }

    const handleClose = () => {
        setAnchorEl(null)
      };

    if (pair === ''){
        return <div></div>
    }

    return (
        <div>
            <AppBar color='primary' position='static' style={{background: '#455a64'}}>
                <Toolbar>
                    <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu" aria-haspopup="true" onClick={handleClick}>
                        <MenuIcon />
                    </IconButton>
                    <Menu 
                        id='pair-menu'
                        anchorEl={anchorEl}
                        keepMounted
                        open={open}
                        onClose={handleClose}
                    >
                        <MenuItem id='BTCUSDT' key='BTCUSDT' onClick={(e) => {setPair(e.target.id); handleClose()}}>BTCUSDT</MenuItem>
                        <MenuItem id='ETHBTC' key='ETHBTC' onClick={(e) => {setPair(e.target.id); handleClose()}}>ETHBTC</MenuItem>
                        <MenuItem id='XRPBTC' key='XRPBTC' onClick={(e) => {setPair(e.target.id); handleClose()}}>XRPBTC</MenuItem>
                        <MenuItem id='TRXBTC' key='TRXBTC' onClick={(e) => {setPair(e.target.id); handleClose()}}>TRXBTC</MenuItem>
                        <MenuItem id='LINKBTC' key='LINKBTC' onClick={(e) => {setPair(e.target.id); handleClose()}}>LINKBTC</MenuItem>
                        <MenuItem id='BATBTC' key='BATBTC' onClick={(e) => {setPair(e.target.id); handleClose()}}>BATBTC</MenuItem>
                    </Menu>
                    <Typography variant="h6" className={classes.title}>
                        Trade Pairs
                    </Typography>
                    <Typography variant="subtitle1" align={'right'} className={classes.title}>
                        trmason.r@gmail.com
                    </Typography>
                </Toolbar>
            </AppBar>
            <br></br> 
            <div className='chartBody'>
                <Paper elevation={10} className={classes.root}>
                    <div className='Chart'>
                        <CoinData pair={pair} />
                    </div>
                    <div className='tradeTable'>
                        <TradeData pair={pair} />
                    </div>
                </Paper>
                <br></br>
            </div>
        </div>
    )
}

export default Chart