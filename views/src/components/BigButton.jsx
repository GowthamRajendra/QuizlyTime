import Card from 'react-bootstrap/Card'
import Col from 'react-bootstrap/Col'

// used on singleplayer/multiplayer and random/usercreated selection pages
export default function BigButton({content, icon, onClick}) {
    return <Col className="d-flex justify-content-center col-12 col-lg-6 fade-in">
                <Card className="text-center clickable-card col-12" onClick={onClick}>
                    <Card.Body>
                        <i className={`bi ${icon}`} style={{fontSize:"7.5em"}}></i>
                        <Card.Title>{content}</Card.Title>
                    </Card.Body>
                </Card>
            </Col>
}