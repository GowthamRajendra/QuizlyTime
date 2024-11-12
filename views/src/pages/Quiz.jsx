import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ProgressBar from 'react-bootstrap/ProgressBar';
import 'bootstrap-icons/font/bootstrap-icons.css'
import { useEffect, useState, useRef } from 'react'
import { useLocation, useNavigate, Navigate } from 'react-router-dom'
import useAuth from '../hooks/useAuth';

import io from 'socket.io-client'

// import useAxios from '../hooks/useAxios'

export default function Quiz() {
    const { auth } = useAuth()

    // Get questions from setup page
    const location = useLocation()
    const questions = location.state.questions

    // server connection
    // const [socket, setSocket] = useState(null)
    const socket = useRef(null)

    // Display current question
    const [questionIndex, setQuestionIndex] = useState(0)
    const questionIndexRef = useRef()
    questionIndexRef.current = questionIndex
    const currQuestion = questions[questionIndexRef.current]

    // User selected answer
    const [selected, setSelected] = useState(null)
    const [submitted, setSubmitted] = useState(false)

    // Correct answer
    const [correct, setCorrect] = useState(null)

    // Timer
    const [timer, setTimer] = useState(-1)

    const navigate = useNavigate()

    useEffect(() => {
        // Connect to the server
        const newSocket = io('http://localhost:5000')
        // setSocket(newSocket)
        socket.current = newSocket

        newSocket.emit('start_quiz', {email: auth.email})
        setTimer(currQuestion.timer)

        newSocket.on('timer_sync', ({time_left}) => {
            // console.log(`timer: ${time_left}`);
            setTimer(time_left)
        })

        newSocket.on('timer_expired', () => {
            console.log('timer expired');
            handleSubmit()
        })
        
        newSocket.on('answer_checked', ({correct_answer, question_index}) => {
            console.log('answer checked');
            console.log(`correct: ${correct_answer}, ${question_index}`);
            console.log(questions[question_index].choices)
            setCorrect(questions[question_index].choices.indexOf(correct_answer))
            setTimer(questions[question_index].timer)
        })        

        newSocket.on('quiz_completed', ({score}) => {
            console.log(`quiz completed: ${score}`);
            console.log(`total questions: ${questions.length}`);
            setTimer(-1)
            setTimeout(() => {
                console.log('navigating to results');
                navigate('/quiz/results', {state: {score: score, total: questions.length}})
            }, 2000)
        });

        // Clean up. Remove the event listener when the component is unmounted
        return () => {
            console.log('cleaning up');
            newSocket.disconnect()
        }
    }, [])

    useEffect(() => {
        const interval = setInterval(() => {

            if (timer >= 0)
            {
                setTimer((prevTime) => prevTime - 1);

                // check every 5 seconds
                if (timer % 5 === 0) {
                    if (socket.current !== null) {
                        console.log('in timer', timer);
                        socket.current.emit('timer_update', 
                        {
                            email: auth.email, 
                            question_timer: currQuestion.timer
                        })
                        console.log('timer sync');     
                    }
                    else {
                        console.log('socket not connected');
                    }
                }
            }
        }, 1000);

        return () => clearInterval(interval); // Cleanup on component unmount
    }, [timer])

    const handleSubmit = () => {
        let user_answer = ''

        if (selected === null && timer > 0) {
            alert('Please select an answer.')
            return
        } 
        else {
            setSubmitted(true)
            if (selected !== null) {
                user_answer = questions[questionIndexRef.current].choices[selected]
            }
        }
        // else {
        //     setSelected(null)
        // }

        // Check if answer is correct
        // Display correct/incorrect
        // socket event to server
        console.log('before emit', questionIndexRef.current);
        console.log(`email: ${auth.email}, question_id: ${questions[questionIndexRef.current].question_id}, user_answer: ${user_answer} question_index: ${questionIndexRef.current}`);
        socket.current.emit('check_answer', { "email": auth.email,  "question_id": questions[questionIndexRef.current].question_id, "user_answer": user_answer, "question_index": questionIndexRef.current})
        console.log('emitted');

        setTimeout(() => {
            console.log('displaying correct answer...');
            setSubmitted(false)

            // Move to next question
            setQuestionIndex(prevIndex => {
                if (prevIndex < questions.length - 1) {
                    console.log('next question', prevIndex);
                    return prevIndex + 1;
                }

                return prevIndex;
            });
            setSelected(null)
            setCorrect(null)
        }, 2000)
    }

    function buttonColor(index) {
        if (index === correct) {
            return 'success'
        }
        else if (index === selected && correct !== null) {
            return 'danger'
        }
        else if (index === selected) {
            return 'primary'
        }
        else {
            return 'outline-primary'
        }
    }

    function resultIcon(index) {
        if (correct !== null) {
            if (index === correct) {
                return <i className="bi bi-check-circle-fill position-absolute end-0 me-5"></i>
            }
            else if (index === selected) {
                return <i className="bi bi-x-circle-fill position-absolute end-0 me-5"></i>
            }
        }
    }

    return (
        // If no questions, redirect to setup page.
        (questions.length === 0 && timer === -2)
        ?
        <Navigate to='/quiz/setup' replace />
          // Question card, with prompt and choices.
        : 
        <Card className='d-flex flex-row justify-content-center w-50 shadow-sm mt-3 bg-dark'>
            <Container>
                <Row className='d-flex flex-row justify-content-end align-items-center mx-3 mt-3'>
                    <Col xs="auto">Time: {timer > 0 ? timer : 0}s</Col>
                </Row>
                <Row className='d-flex flex-row justify-content-center mx-3 mt-3'>
                <Col xs={12}>
                    <ProgressBar now={timer} max={currQuestion.timer}/>
                </Col>
                </Row>
                <Row className='d-flex flex-row justify-content-center mx-3 mt-3'>
                    <h3>{questionIndex+1}. {currQuestion.prompt}</h3>
                </Row>
                <Row className='d-flex flex-row row-gap-3 mx-3 mt-3'>
                    {currQuestion.choices.map((choice, index) => {
                        return <Button key={index} 
                        variant={buttonColor(index)} 
                        onClick={() => setSelected(index)}
                        disabled={submitted}>
                            {choice} 
                            {resultIcon(index)}
                        </Button>
                    })}
                </Row>
                <hr />
                <Row className='d-flex flex-row justify-content-between align-items-center mb-3'>
                    <Col xs="auto">Question {questionIndex+1} of {questions.length}</Col>
                    <Col xs="auto"><Button variant='primary' 
                    onClick={() => {handleSubmit()}} 
                    disabled={submitted}>Submit</Button></Col>
                </Row>
            </Container>
        </Card>
    )
}
