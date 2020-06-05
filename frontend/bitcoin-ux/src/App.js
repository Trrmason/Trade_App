import React from 'react'
import Chart from './components/chart/Chart'
import Bar from './components/head/Bar'
import Footer from './components/footer/Footer'

const App = () => (
    <div>
        <Bar />
        <div className='chartBody'>
            <Chart />
        </div>
        <Footer />
    </div>
)


export default App