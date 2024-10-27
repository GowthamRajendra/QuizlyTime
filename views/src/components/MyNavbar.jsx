import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

function MyNavbar() {
    return (
        <Navbar className='ms-3'>
            <Navbar.Brand href='/home'>Home</Navbar.Brand>
            <Nav>
                <Nav.Link href='/login'>Login</Nav.Link>
                <Nav.Link href='/register'>Register</Nav.Link>
            </Nav>
        </Navbar>
    )
}

export default MyNavbar;