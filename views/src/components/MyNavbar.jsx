import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

function MyNavbar() {
    const { auth } = useAuth()

    return (
        <Navbar className='ms-3'>
            <Link to='/' className='navbar-brand'>Home</Link>
            <Nav>
                {
                    !auth ?   
                    [<Link to="/login" className='nav-link'>Login</Link>,
                    <Link to="/register" className='nav-link'>Register</Link>]
                    : <Link to="/quiz" className='nav-link'>Play</Link>
                }
            </Nav>
        </Navbar>
    )
}

export default MyNavbar;