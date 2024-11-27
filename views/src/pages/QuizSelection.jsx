import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom'

import useAxios from "../hooks/useAxios";
import useAuth from "../hooks/useAuth";

import QuizTab from "../components/QuizTab";

import '../quiz.css';

export default function QuizSelection (){
    const axios = useAxios();
    const navigate = useNavigate()
    
    const [ quizzes, setQuizzes ] = useState([]);

    useEffect(() => {
        const getCustomQuizzes = async () => {
            try {
                const response = await axios.get('/get-custom-quizzes');
                console.log(`Retrieved: ${JSON.stringify(response.data)}`);
                setQuizzes(response.data.quizzes.reverse());
            } catch (error) {
                console.error(error);
            }
        }

        getCustomQuizzes();

        return () => {
            console.log('cleaning up');
        }
    }, []);

    return (
        <div className="w-100 d-flex flex-column align-items-center" style={{ maxWidth: '1200px', margin: '0 auto' }}>
            <Row className="w-100">
                <Col>
                    <h2>Select Quiz To Play</h2>
                        <ul>
                            {quizzes.map((quiz, index) => (
                                <li key={index} className="clickable-card mb-1" onClick={() => navigate('/quiz/play', {state: {questions: quiz.questions}})}>
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
        </div>
    );

}