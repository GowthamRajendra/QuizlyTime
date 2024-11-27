import useAuth from "../hooks/useAuth";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Modal from "react-bootstrap/Modal";
import useAxios from "../hooks/useAxios";
import { useEffect, useState } from "react";
import QuizTab from "../components/QuizTab";
import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";

function Profile() {
    const { auth } = useAuth();
    const axios = useAxios();
    const initial = auth.username.charAt(0).toUpperCase();

    // Tab control
    const [ activeTab, setActiveTab ] = useState('History');

    // Quizzes played history
    const [ history, setHistory ] = useState([]);

    // Quizzes created by this user
    const [ creations, setCreations ] = useState([]);

    // Player stats
    const [ gamesPlayed, setGamesPlayed ] = useState(0);
    const [ avgScore, setAvgScore ] = useState(0);

    // for editing quiz
    const [index, setIndex] = useState(0);
    const [newTitle, setNewTitle] = useState('');

    // modal
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    // Get history and creations
    useEffect(() => {
        const getHistory = async () => {
            try {
                const response = await axios.get('/profile/history');
                console.log(`Retrieved: ${JSON.stringify(response.data)}`);
                setHistory(response.data.quizzes.reverse());
                
                // Calculate player stats
                setGamesPlayed(response.data.quizzes.length);
                let totalScore = 0;
                response.data.quizzes.forEach(quiz => {
                    totalScore += quiz.score / (quiz.total_questions * 10);
                });

                if (response.data.quizzes.length !== 0) {
                    setAvgScore(Math.round(100*totalScore / response.data.quizzes.length));
                }
                
            } catch (error) {
                console.error(error);
            }
        }

        const getCreations = async () => {
            try {
                const response = await axios.get('/profile/creations');
                console.log(`Retrieved: ${JSON.stringify(response.data)}`);
                setCreations(response.data.quizzes.reverse());
            } catch (error) {
                console.error(error);
            }
        }

        getHistory();
        getCreations();

        return () => {
            console.log('cleaning up');
        }
    }, []);

    const editQuiz = async () => {
        console.log(`Edit quiz: ${JSON.stringify(creations[index])}`);

        try {
            const response = await axios.put(`/edit-custom-quiz`, {
                quiz_id: creations[index].id,
                title: newTitle,
            });

            console.log(`Response: ${JSON.stringify(response.data)}`);

            // Update the quiz in the state
            let newCreations = [...creations];
            newCreations[index].title = newTitle;
            setCreations(newCreations);

        } catch (error) {
            console.error(error);
        }
    }

    const deleteQuiz = async (index) => {
        console.log(`Delete quiz: ${JSON.stringify(creations[index])}`);

        try {
            const response = await axios.delete(`/delete-custom-quiz`, {
                data: {
                    quiz_id: creations[index].id,
                }
            });

            console.log(`Response: ${JSON.stringify(response.data)}`);

            // Update the quiz in the state
            let newCreations = [...creations];
            newCreations.splice(index, 1);
            setCreations(newCreations);

        } catch (error) {
            console.error(error);
        }
    }

    return (

        <>
        <Modal show={show} onHide={() => {handleClose(); setNewTitle('')}}>
            <Modal.Header closeButton>
                <Modal.Title>Change Quiz Title</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className="mb-3" controlId="newTitleForm">
                    <Form.Label>New Title</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Quiz 1"
                        autoFocus
                        value={newTitle}
                        onChange={(e) => setNewTitle(e.target.value)}
                    />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={() => {handleClose(); setNewTitle('')}}>
                    Close
                </Button>
                <Button variant="primary" onClick={() => {handleClose(); editQuiz()}}>
                    Save
                </Button>
            </Modal.Footer>
        </Modal>
    
        <div className="w-100 d-flex flex-column align-items-center" style={{ maxWidth: '1200px', margin: '0 auto' }}>
            {/* Profile header */}
            <Row className="w-100 d-flex align-items-center">
                <Col xs="auto" className="d-flex align-items-center">
                    <div
                        className="d-flex justify-content-center align-items-center bg-primary text-white rounded-circle"
                        style={{
                            width: '150px',
                            height: '150px',
                            fontSize: '50px',
                            fontWeight: 'bold',
                        }}
                    >
                        <h1>{initial}</h1>
                    </div>
                </Col>
                <Col className="d-flex align-items-center">
                    <h1 className="m-0">{auth.username}</h1>
                </Col>
                <Col className="d-flex justify-content-start">
                    <div>
                        <h3>Games played: {gamesPlayed}</h3>
                        <h3>Avg score: {avgScore}%</h3>
                    </div>
                </Col>
            </Row>

            {/* Tabs: History and Creations */}
            <Row className="w-100 mt-3">
                <Tabs
                    id="profile-tabs"
                    activeKey={activeTab}
                    onSelect={(k) => setActiveTab(k)}
                    className="w-100"
                >
                    <Tab eventKey={"History"} title="History">
                        <Row className="w-100">
                            <Col>
                                <h2 className="mx-5 mt-3">Quizzes Played</h2>
                                <ul>
                                    {history.map((quiz, index) => (
                                        <li key={index} className="mb-1 w-75">
                                            <QuizTab
                                                title={quiz.title}
                                                score={quiz.score}
                                                total_questions={quiz.total_questions}
                                                timestamp={quiz.timestamp}
                                            />
                                        </li>
                                    ))}
                                </ul>
                            </Col>
                        </Row>
                    </Tab>
                    <Tab eventKey={"Your Creations"} title="Your Creations">
                        <Row className="w-100">
                            <Col>
                                <h2 className="mx-5 mt-3">Created Quizzes</h2>
                                <ul>
                                    {creations.map((quiz, index) => (
                                        <li key={index} className="mb-1 w-75">
                                            <Row>
                                                <Col>
                                                    <div style={{ position: 'relative' }}>
                                                        <QuizTab
                                                            title={quiz.title}
                                                            total_questions={quiz.total_questions}
                                                            timestamp={quiz.timestamp}
                                                        />
                                                        <div style={{ position: 'absolute', top: '15px', right: '70px', zIndex: 10 }}>
                                                            <Button variant="dark" onClick={() => {handleShow(); setIndex(index)}}>
                                                                <i className="bi bi-pencil-square h3"></i>
                                                            </Button>
                                                        </div>
                                                        <div style={{ position: 'absolute', top: '15px', right: '10px', zIndex: 10 }}>
                                                            <Button variant="dark" onClick={() => deleteQuiz(index)}>
                                                                <i className="bi bi-trash h3"></i>
                                                            </Button>
                                                        </div>
                                                    </div>
                                                </Col>
                                            </Row>
                                        </li>
                                    ))}
                                </ul>
                            </Col>
                        </Row>
                    </Tab>
                </Tabs>
            </Row>
        </div>

    </>
    );
}

export default Profile;