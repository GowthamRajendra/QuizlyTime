import useAuth from "../hooks/useAuth";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
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

    return (
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
                                        <li key={index} className="mb-1">
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
                                <h2 className="mx-5 mt-3">Quizzes Created</h2>
                                <ul>
                                    {creations.map((quiz, index) => (
                                        <li key={index} className="mb-1">
                                            <QuizTab
                                                title={quiz.title}
                                                total_questions={quiz.total_questions}
                                                timestamp={quiz.timestamp}
                                            />
                                        </li>
                                    ))}
                                </ul>
                            </Col>
                        </Row>
                    </Tab>
                </Tabs>
            </Row>
        </div>
    );
}

export default Profile;