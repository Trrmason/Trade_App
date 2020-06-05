import React from 'react'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'

function Bar(){
    return (
        <div>
            <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
            <Navbar.Brand>Trade-App</Navbar.Brand>
            <Navbar.Toggle aria-controls="responsive-navbar-nav" />
            <Navbar.Collapse id="responsive-navbar-nav">
                <Nav className="mr-auto">
                <Nav.Link>Travis.Mason</Nav.Link>
                </Nav>
            </Navbar.Collapse>
            </Navbar>
        </div>
    )
}



export default Bar