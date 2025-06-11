import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Modal from "react-bootstrap/Modal";
import useAxios from "../hooks/useAxios";
import QuizTab from "../components/QuizTab";
import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";
import ListGroup from "react-bootstrap/ListGroup";
import Pagination from "react-bootstrap/Pagination";
import Loading from "../components/Loading";

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import useAuth from "../hooks/useAuth";


function Profile() {
    const { auth } = useAuth();
    const axios = useAxios();
    const navigate = useNavigate();

    const initial = auth.username.charAt(0).toUpperCase();

    // Tab control
    const [ activeTab, setActiveTab ] = useState('History');

    // Quizzes played history
    const [ history, setHistory ] = useState([]);
    const [indexOfLastHistory, setIndexOfLastHistory] = useState(0);
    const [indexOfFirstHistory, setIndexOfFirstHistory] = useState(0);

    // Quizzes created by this user
    const [ creations, setCreations ] = useState([]);
    const [indexOfLastCreation, setIndexOfLastCreation] = useState(0);
    const [indexOfFirstCreation, setIndexOfFirstCreation] = useState(0);

    // Player stats
    const [ gamesPlayed, setGamesPlayed ] = useState(0);
    const [ avgScore, setAvgScore ] = useState(0);

    // for editing quiz
    const [index, setIndex] = useState(0);
    const [newTitle, setNewTitle] = useState('');

    // modal
    const [show, setShow] = useState(false);

    const [loading, setLoading] = useState(true);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    // Get history and creations
    useEffect(() => {
        const getHistory = async () => {
            try {
                setLoading(true);
                const response = await axios.get('/profile/history');
                setLoading(false);
                console.log(`Retrieved: ${JSON.stringify(response.data)}`);
                setHistory(response.data.quizzes);
                
                // Calculate player stats
                setGamesPlayed(response.data.quizzes.length);
                let totalScore = 0;
                response.data.quizzes.forEach(quiz => {
                    totalScore += quiz.score / (quiz.total_questions * 10);
                });

                if (response.data.quizzes.length !== 0) {
                    setAvgScore(Math.round(100*totalScore / response.data.quizzes.length));
                }
                setIndexOfFirstHistory(0);
                setIndexOfLastHistory(5);
            } catch (error) {
                setLoading(false);
                console.error(error);
            }
        }

        const getCreations = async () => {
            try {
                setLoading(true);
                const response = await axios.get('/profile/creations');
                setLoading(false);
                console.log(`Retrieved: ${JSON.stringify(response.data)}`);
                setCreations(response.data.quizzes.reverse());

                setIndexOfFirstCreation(0);
                setIndexOfLastCreation(5);
            } catch (error) {
                setLoading(false);
                console.error(error);
            }
        }

        getHistory();
        getCreations();

        return () => {
            console.log('cleaning up');
        }
    }, []);

    const editQuiz = async (edit) => {
        console.log(`Edit quiz: ${JSON.stringify(creations[index])}`);

        try {
            const response = await axios.put(`/edit-custom-quiz-title`, {
                quiz_id: creations[index].id,
                title: newTitle,
            });

            console.log(`Response: ${JSON.stringify(response.data)}`);

            // Update the quiz in the state
            let newCreations = [...creations];
            newCreations[index].title = newTitle;
            setCreations(newCreations);

            let new_questions = []

            // format questions
            response.data.questions.forEach((question) => {
                new_questions.push({
                    prompt: question.prompt,
                    categorySelect: false,
                    category: question.category,
                    difficulty: question.difficulty,
                    multiple: true ? question.type === "multiple" : false,
                    choices: question.incorrect_answers,
                    answer: question.correct_answer,
                    question_id: question.question_id
                })
            })

            console.log(`New questions: ${JSON.stringify(new_questions)}`);

            if (edit) {
                navigate('/quiz/create/questions', {state: {title: newTitle, questions: new_questions, quiz_id: creations[index].id}});
            }

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

    if (loading) {
        return <Loading />
    }

    return (

        <>
        <Modal show={show} onHide={() => {handleClose(); setNewTitle('')}}>
            <Modal.Header closeButton>
                <Modal.Title>Edit Quiz</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className="mb-3" controlId="newTitleForm">
                    <Form.Label>New Title</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Quiz 1"
                        autoFocus
                        defaultValue={newTitle}
                        onChange={(e) => e.target.value.length > 0 ? setNewTitle(e.target.value) : setNewTitle(newTitle)}
                        maxLength={37}
                        required
                    />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer className="d-flex justify-content-between">
                <Button variant="success" onClick={() => {handleClose(); editQuiz(false)}}>
                    Save Title and Exit
                </Button>
                <Button variant="primary" onClick={() => {handleClose(); editQuiz(true)}}>
                    Continue to Edit Questions
                </Button>
            </Modal.Footer>
        </Modal>
    
        <div className="w-100 d-flex flex-column align-items-center" style={{ maxWidth: '1200px', margin: '0 auto' }}>
            {/* Profile header */}
            <Row className="w-100 d-flex align-items-center">
                <Col className="d-flex justify-content-center align-items-center col-12 col-sm-6 gap-3">
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
                    <h1 className="m-0">{auth.username}</h1>
                </Col>
                <Col className="d-flex justify-content-center col-12 col-sm-6">
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
                    justify={true}
                >
                    {/* History Tab */}
                    <Tab eventKey={"History"} title="History" className="justify-content-center">
                        <Row className="w-100 m-0 p-0">
                            {/* Structure: Title, pagination, content, pagination */}
                            <Col className="d-flex flex-column align-items-center">
                                <h2 className="my-3">Quizzes Played</h2>
                                <Pagination className="mt-2" hidden={history.length <= 5}>
                                    <Pagination.Prev 
                                        disabled={indexOfFirstHistory === 0}
                                        onClick={() => {
                                            if (indexOfFirstHistory > 0) {
                                                setIndexOfFirstHistory(indexOfFirstHistory - 5);
                                                setIndexOfLastHistory(indexOfLastHistory - 5);
                                            }
                                        }} 
                                    />
                                    <Pagination.Next 
                                        disabled={indexOfLastHistory >= history.length}
                                        onClick={() => {
                                            if (indexOfLastHistory < history.length) {
                                                setIndexOfFirstHistory(indexOfFirstHistory + 5);
                                                setIndexOfLastHistory(indexOfLastHistory + 5);
                                            }
                                        }} 
                                    />  
                                </Pagination>
                                <ListGroup className="w-100">
                                    {history.slice(indexOfFirstHistory, indexOfLastHistory).map((quiz, index) => (
                                        <QuizTab
                                            key={index}
                                            title={quiz.title}
                                            score={quiz.score}
                                            total_questions={quiz.total_questions}
                                            timestamp={quiz.timestamp}
                                            animOrder={index % 5}
                                        />
                                    ))}
                                </ListGroup>
                                <Pagination className="mt-2" hidden={history.length <= 5}>
                                    <Pagination.Prev 
                                        disabled={indexOfFirstHistory === 0}
                                        onClick={() => {
                                            if (indexOfFirstHistory > 0) {
                                                setIndexOfFirstHistory(indexOfFirstHistory - 5);
                                                setIndexOfLastHistory(indexOfLastHistory - 5);
                                            }
                                        }} 
                                    />
                                    <Pagination.Next 
                                        disabled={indexOfLastHistory >= history.length}
                                        onClick={() => {
                                            if (indexOfLastHistory < history.length) {
                                                setIndexOfFirstHistory(indexOfFirstHistory + 5);
                                                setIndexOfLastHistory(indexOfLastHistory + 5);
                                            }
                                        }} 
                                    />
                                </Pagination>
                            </Col>
                        </Row>
                    </Tab>
                    {/* Creations Tab */}
                    <Tab eventKey={"Your Creations"} title="Your Creations">
                        <Row className="w-100 m-0 p-0">
                            {/* Structure: Title, pagination, content, pagination */}
                            <Col className="d-flex flex-column align-items-center">
                                <h2 className="my-3">Created Quizzes</h2>
                                <Pagination hidden={creations.length <= 5}>
                                    <Pagination.Prev 
                                        disabled={indexOfFirstCreation === 0}
                                        onClick={() => {
                                            if (indexOfFirstCreation > 0) {
                                                setIndexOfFirstCreation(indexOfFirstCreation - 5);
                                                setIndexOfLastCreation(indexOfLastCreation - 5);
                                            }
                                        }} 
                                    />
                                    <Pagination.Next 
                                        disabled={indexOfLastCreation >= creations.length}
                                        onClick={() => {
                                            if (indexOfLastCreation < creations.length) {
                                                setIndexOfFirstCreation(indexOfFirstCreation + 5);
                                                setIndexOfLastCreation(indexOfLastCreation + 5);
                                            }
                                        }} 
                                    />
                                </Pagination>
                                <ListGroup className="w-100">
                                    {creations.slice(indexOfFirstCreation, indexOfLastCreation).map((quiz, index) => (
                                        <Row key={index} className="fade-in" style={{"--animation-order": index % 5}}>
                                            <Col>
                                                <div style={{ position: 'relative' }}>
                                                    <QuizTab
                                                        title={quiz.title}
                                                        total_questions={quiz.total_questions}
                                                        timestamp={quiz.timestamp}
                                                    />
                                                    <div style={{ position: 'absolute', top: '15px', right: '70px', zIndex: 10 }}>
                                                        <Button variant="dark" onClick={() => {handleShow(); setIndex(index); setNewTitle(quiz.title)}}>
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
                                    ))}
                                </ListGroup>
                                <Pagination hidden={creations.length <= 5}>
                                    <Pagination.Prev 
                                        disabled={indexOfFirstCreation === 0}
                                        onClick={() => {
                                            if (indexOfFirstCreation > 0) {
                                                setIndexOfFirstCreation(indexOfFirstCreation - 5);
                                                setIndexOfLastCreation(indexOfLastCreation - 5);
                                            }
                                        }} 
                                    />
                                    <Pagination.Next 
                                        disabled={indexOfLastCreation >= creations.length}
                                        onClick={() => {
                                            if (indexOfLastCreation < creations.length) {
                                                setIndexOfFirstCreation(indexOfFirstCreation + 5);
                                                setIndexOfLastCreation(indexOfLastCreation + 5);
                                            }
                                        }} 
                                    />
                                </Pagination>
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