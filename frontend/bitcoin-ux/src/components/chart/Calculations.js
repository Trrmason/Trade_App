import React, {useState, useEffect} from 'react'
import TableContainer from '@material-ui/core/TableContainer';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';


const useStyles = makeStyles({
    root: {
      width: '100%',
    },
    container: {
      maxHeight: 650,
    },
    tableCell: {
        paddingRight: 4,
        panddingLeft: 5
    }
 });


function tradeCalculations(data){
    let winPercent = 0
    let percentLong = 0
    let percentShort = 0
    for (let i = data.length-1; i > 0; i--){
        if (i >= 1){
            let prev = data[i]
            let curr = data[i-1]
            if (prev.decision === 'Buy'){
                if (prev.closePrice < curr.closePrice) {
                    winPercent += 1
                }
                percentLong += ((curr.closePrice - prev.closePrice) / prev.closePrice) * 100 
            } else {
                if (prev.closePrice > curr.closePrice) {
                    winPercent += 1
                }
                percentShort += ((curr.closePrice - prev.closePrice) / prev.closePrice) * -100 
            } 
        } 
    }
    return ({'winPercent': ((winPercent / (data.length-1)) * 100.0).toFixed(2), 'percentLong': percentLong.toFixed(2),'percentShort': percentShort.toFixed(2)})
}


function Calculations(props){

    const [calc, setCalc] = useState({winPercent: '', percentLong: '', percentShort:''})
    const classes = useStyles();

    useEffect(() => {
        if (props.trades.length > 1){
            const data = tradeCalculations(props.trades)
            setCalc({'winPercent': data.winPercent, 'percentLong': data.percentLong, 'percentShort': data.percentShort})
        }
    }, [props])
        
    return (
        <TableContainer className={classes.container}>
         <Table size='small' stickyHeader aria-label="sticky table">
            <TableHead>
                <TableRow>
                    <TableCell 
                        align={'left'}
                        >Win % </TableCell>
                    <TableCell 
                        align={'left'}
                        >Long % </TableCell>
                    <TableCell 
                        align={'left'}
                        >Short % </TableCell>
                </TableRow>
            </TableHead>
                <TableBody>
                    <TableRow hover key={calc.winPercent}  tabIndex={-1} align={'left'}>
                        <TableCell className={classes.TableCell} 
                                    align={'left'} 
                                    style={{color: (calc.winPercent > 0) ? '#00c853' : 'red'}}> {calc.winPercent}</TableCell>
                        <TableCell className={classes.TableCell} 
                                    align={'left'} 
                                    style={{color: (calc.percentLong > 0) ? '#00c853' : 'red'}}> {calc.percentLong}</TableCell>
                        <TableCell className={classes.TableCell} 
                                    align={'left'} 
                                    style={{color: (calc.percentShort > 0) ? '#00c853' : 'red'}}> {calc.percentShort}</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </TableContainer>
        )
}





export default Calculations