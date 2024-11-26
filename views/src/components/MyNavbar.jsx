import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from 'react-router-dom';
import useAuth from '../hooks/useAuth';
import useLogout from '../hooks/useLogout';

function MyNavbar() {
    const { auth } = useAuth()
    const { logout } = useLogout()

    return (
        <Navbar className='ms-3'>
            <Link to='/' className='navbar-brand' key={0}>Home</Link>
            <Nav>
                {
                    !auth   
                    ? [<Link to="/login" className='nav-link' key={1}>Login</Link>,
                    <Link to="/register" className='nav-link' key={2}>Register</Link>]
                    : [<Link to="/quiz/setup" className='nav-link' key={3}>Play</Link>,
                    <Link to="/quiz/create/setup" className='nav-link' key={4}>Create</Link>,
                    <Link to="/" className='nav-link' onClick={logout} key={5}>Logout</Link>]
                }
            </Nav>
        </Navbar>
    )
}

export default MyNavbar;