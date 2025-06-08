import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from 'react-router-dom';
import useAuth from '../hooks/useAuth';
import useLogout from '../hooks/useLogout';

function MyNavbar() {
    const { auth } = useAuth()
    const { logout } = useLogout()

    return (
        <Navbar className='mb-4 slide-down z-1' style={{backgroundColor: '#000000'}}>
            <Link to='/' className='navbar-brand mx-3' key={0}>Quizly Time</Link>
            <Nav>
                {
                    !auth   
                    ? [<Link to="/login" id='loginNav' className='nav-link' key={1}>Login</Link>,
                    <Link to="/register" id='registerNav' className='nav-link' key={2}>Register</Link>]
                    : [<Link to="/quiz" id='playNav' className='nav-link' key={3}>Play</Link>,
                    <Link to="/quiz/create/setup" id='createNav' className='nav-link' key={4}>Create</Link>,
                    <Link to="/" id='logoutNav' className='nav-link' onClick={logout} key={5}>Logout</Link>,
                    <Link to="/multiplayer" id='multiplayerNav' className='nav-link' key={6}>Multiplayer</Link>]
                }
            </Nav>
        </Navbar>
    )
}

export default MyNavbar;