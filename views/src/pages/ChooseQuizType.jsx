import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import 'bootstrap-icons/font/bootstrap-icons.css'
import '../quiz.css'
import BigButton from '../components/BigButton';

import { useNavigate } from 'react-router-dom'

export default function ChooseQuizType() {
    const navigate = useNavigate()

    return (
        <Container className="d-flex justify-content-center align-items-start">
            <Row className='col-12 col-lg-6'>
                <BigButton content={"Create Random Quiz"} icon="bi-dice-5-fill" onClick={() => navigate('/singleplayer/setup')} />
                <BigButton content={"Choose a Quiz"} icon="bi-archive-fill" onClick={() => navigate('/singleplayer/select')}/>
            </Row>
        </Container>
      );

}