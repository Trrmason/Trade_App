import React from 'react'
import Navbar from 'react-bootstrap/Navbar'


function Footer(){
    return(
        <div className='Footer'>
            <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
            <p className='footerText'>trmason.r@gmail.com</p>
            <Navbar.Toggle aria-controls="responsive-navbar-nav" />
            </Navbar>
        </div>
    )

}



export default Footer