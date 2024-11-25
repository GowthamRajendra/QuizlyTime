import useAuth from "../hooks/useAuth";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import useAxios from "../hooks/useAxios";
import { useEffect, useState } from "react";
import QuizTab from "../components/QuizTab";

function Profile() {
    const { auth } = useAuth();
    const axios = useAxios();
    const initial = auth.username.charAt(0).toUpperCase();
    const [ quizzes, setQuizzes ] = useState([]);
    const [ gamesPlayed, setGamesPlayed ] = useState(0);
    const [ avgScore, setAvgScore ] = useState(0);

    // Get previously played quizzes
    useEffect(() => {
        const getQuizzes = async () => {
            try {
                const response = await axios.get('/profile/retrieve_quizzes');
                console.log(`Retrieved: ${JSON.stringify(response.data)}`);
                setQuizzes(response.data.quizzes);

                setGamesPlayed(response.data.quizzes.length);
                let totalScore = 0;
                response.data.quizzes.forEach(quiz => {
                    totalScore += quiz.score / (quiz.total_questions * 10);
                });
                setAvgScore(Math.round(100*totalScore / response.data.quizzes.length));
                
            } catch (error) {
                console.error(error);
            }
        }

        getQuizzes();

        return () => {
            console.log('cleaning up');
        }
    }, []);

    return (
        <div className="w-100">
            <Row className="d-flex align-items-center ms-4">
                <Col xs="auto" className="d-flex align-items-center w-auto">
                    <div className="d-flex justify-content-center align-items-center bg-primary text-white rounded-circle"
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
            <Row>
                <Col>
                    <h2 class="mx-5 mt-3">Quizzes Played</h2>
                    <ul>
                        {
                            quizzes.map((quiz, index) => {
                                return (
                                    <li key={index}>
                                        <QuizTab 
                                            title={quiz.title} 
                                            score={quiz.score} 
                                            total_questions={quiz.total_questions} 
                                            timestamp={quiz.timestamp}
                                        />
                                    </li>
                                );
                            })
                        }
                    </ul>
                </Col>
            </Row>
        </div>
    );
}

export default Profile;