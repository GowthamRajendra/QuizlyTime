import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Pagination from "react-bootstrap/Pagination";
import ListGroup from "react-bootstrap/ListGroup";

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
    const [ indexOfFirstQuiz, setIndexOfFirstQuiz ] = useState(0);
    const [ indexOfLastQuiz, setIndexOfLastQuiz ] = useState(5);


    useEffect(() => {
        const getCustomQuizzes = async () => {
            try {
                const response = await axios.get('/get-custom-quizzes');
                // console.log(`Retrieved: ${JSON.stringify(response.data)}`);
                setQuizzes(response.data.quizzes.reverse());

                setIndexOfFirstQuiz(0);
                setIndexOfLastQuiz(5);
            } catch (error) {
                console.error(error);
            }
        }

        getCustomQuizzes();

        return () => {
            console.log('cleaning up');
        }
    }, []);

    const playQuiz = async (index) => {
        try {
            const response = await axios.post('/begin-quiz', {quiz_id: quizzes[index].id});
            console.log(`Retrieved: ${JSON.stringify(response.data)}`);
            navigate('/quiz/play', {state: {questions: quizzes[index].questions}});
        } catch (error) {
            console.error(error);
        }
    }

    return (
        <div className="w-100">
            <Col className="w-100 m-0 p-0 d-flex flex-column align-items-center">
                <h2>Select Quiz To Play</h2>
                    <ListGroup className="w-100 d-flex flex-column align-items-center">
                        {quizzes.slice(indexOfFirstQuiz, indexOfLastQuiz).map((quiz, index) => (
                            <div key={index} className="mb-1 clickable-card w-75"
                                    onClick={() => playQuiz(index)}>
                                    <QuizTab
                                        title={quiz.title}
                                        total_questions={quiz.total_questions}
                                        timestamp={quiz.timestamp}
                                    />
                            </div>
                        ))}
                    </ListGroup>
                    <Pagination className="mt-2" hidden={history.length <= 5}>
                        <Pagination.Prev 
                            disabled={indexOfFirstQuiz === 0}
                            onClick={() => {
                                if (indexOfFirstQuiz > 0) {
                                    setIndexOfFirstQuiz(indexOfFirstQuiz - 5);
                                    setIndexOfLastQuiz(indexOfLastQuiz - 5);
                                }
                            }} 
                        />
                        <Pagination.Next 
                            disabled={indexOfLastQuiz >= history.length}
                            onClick={() => {
                                if (indexOfLastQuiz < history.length) {
                                    setIndexOfFirstQuiz(indexOfFirstQuiz + 5);
                                    setIndexOfLastQuiz(indexOfLastQuiz + 5);
                                }
                            }} 
                        />
                    </Pagination>
            </Col>
        </div>
    );

}