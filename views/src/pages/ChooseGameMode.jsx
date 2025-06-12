import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import 'bootstrap-icons/font/bootstrap-icons.css'
import '../quiz.css'
import BigButton from '../components/BigButton';

import { useNavigate } from 'react-router-dom'

export default function ChooseGameMode() {
    const navigate = useNavigate()

    return (
        <Container className="d-flex justify-content-center align-items-start">
            <Row className='col-12 col-lg-6'>
                <BigButton content={"Singleplayer"} icon="bi-person-fill" onClick={() => navigate('/singleplayer')} />
                <BigButton content={"Mutliplayer"} icon="bi-people-fill" onClick={() => navigate('/multiplayer')}/>
            </Row>
        </Container>
      );

}