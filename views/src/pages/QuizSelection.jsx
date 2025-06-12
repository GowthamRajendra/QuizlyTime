import Col from "react-bootstrap/Col";
import Pagination from "react-bootstrap/Pagination";
import ListGroup from "react-bootstrap/ListGroup";
import Loading from "../components/Loading";

import { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom'

import useAxios from "../hooks/useAxios";

import QuizTab from "../components/QuizTab";

import '../quiz.css';

export default function QuizSelection (){
    const axios = useAxios();
    const navigate = useNavigate()
    
    const [ quizzes, setQuizzes ] = useState([]);
    const [ indexOfFirstQuiz, setIndexOfFirstQuiz ] = useState(0);
    const [ indexOfLastQuiz, setIndexOfLastQuiz ] = useState(5);

    const [ loading, setLoading ] = useState(true);


    useEffect(() => {
        const getCustomQuizzes = async () => {
            try {
                const response = await axios.get('/get-custom-quizzes');
                setLoading(false);
                // console.log(`Retrieved: ${JSON.stringify(response.data)}`);
                setQuizzes(response.data.quizzes.reverse());

                setIndexOfFirstQuiz(0);
                setIndexOfLastQuiz(5);
            } catch (error) {
                setLoading(false);
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
            setLoading(true);
            const response = await axios.post('/begin-quiz', {quiz_id: quizzes[index].id});
            console.log(`Retrieved: ${JSON.stringify(response.data)}`);
            navigate('/singleplayer/play', {state: {questions: quizzes[index].questions}});
        } catch (error) {
            setLoading(false);
            console.error(error);
        }
    }

    if (loading) {
        return <Loading />
    }

    return (
        <div className="w-100">
            <Col className="w-100 m-0 p-0 d-flex flex-column align-items-center">
                <h2>Select Quiz To Play</h2>
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
                    <ListGroup className="w-100 d-flex flex-column align-items-center">
                        {quizzes.slice(indexOfFirstQuiz, indexOfLastQuiz).map((quiz, index) => (
                            <div key={index} className="mb-1 clickable-card w-75"
                                    onClick={() => playQuiz(index)}>
                                    <QuizTab
                                        title={quiz.title}
                                        total_questions={quiz.total_questions}
                                        timestamp={quiz.timestamp}
                                        animOrder={index % 5}
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