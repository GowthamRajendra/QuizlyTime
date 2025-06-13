import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ProgressBar from 'react-bootstrap/ProgressBar'
import 'bootstrap-icons/font/bootstrap-icons.css'
import { useEffect, useState } from 'react'
import { useLocation, useNavigate, Navigate, replace } from 'react-router-dom'
import useAuth from '../hooks/useAuth';

import io from 'socket.io-client'

// import useAxios from '../hooks/useAxios'

export default function Quiz() {
    const { auth } = useAuth()

    // Get questions from setup page
    const location = useLocation()
    const questions = location.state?.questions ?? []

    console.log("QUIZ QUESTIONS: ", questions);

    // server connection
    const [socket, setSocket] = useState(null)

    // Display current question
    const [questionIndex, setQuestionIndex] = useState(0)
    const currQuestion = questions[questionIndex]

    // User selected answer
    const [selected, setSelected] = useState(null)
    const [submitted, setSubmitted] = useState(false)

    // Correct answer
    const [correct, setCorrect] = useState(null)

    // Timer for question
    const [timer, setTimer] = useState(currQuestion?.timer ?? 0)
    const [maxTime, setMaxTime] = useState(timer)

    const navigate = useNavigate()

    // Set up socket connection and events
    useEffect(() => {
        // Connect to the server
        const newSocket = io(`${import.meta.env.VITE_SOCKET_URL || 'http://localhost:5000'}/singleplayer`,
            {
                transports:['websocket'],
                withCredentials: true
            })
        setSocket(newSocket)

        console.log(`${auth.email}, ${auth.username} connected to quiz`);

        const handleAnswerChecked = ({correct_answer, question_index}) => {
            console.log('answer checked');
            console.log(`correct: ${correct_answer}, ${question_index}`);
            console.log(questions[question_index].choices)
            setCorrect(questions[question_index].choices.indexOf(correct_answer))
        }
        
        const handleNextQuestion = () => {
            console.log('displaying correct answer...');
            setSubmitted(false)
            setSelected(null)
            console.log(`CURRENT INDEX: ${questionIndex}`)
            setQuestionIndex((prevQIndex) => prevQIndex+1)
            setCorrect(null)
            
            // reset timer
            setTimer(questions[questionIndex].timer)
            setMaxTime(questions[questionIndex].timer)
        }
        
        const handleQuizCompleted = ({score}) => {
            console.log(`quiz completed: ${score}`);
            console.log(`total questions: ${questions.length}`);

            navigate('/singleplayer/results', {replace: true, state: {score: score, total: questions.length*10}})
        }
        
        newSocket.on('connect', () => {
            console.log("CONNECTED TO SINGLEPLAYER")
        })
        newSocket.on('answer_checked', handleAnswerChecked)        
        newSocket.on('next_question', handleNextQuestion)
        newSocket.on('quiz_completed', handleQuizCompleted)

        // Clean up. Remove the event listener when the component is unmounted
        return () => {
            console.log('cleaning up');
            newSocket.disconnect()
        }
    }, [])

    // Handle answer submission
    const handleSubmit = () => {
        let user_answer = ''

        if (selected === null && timer > 0) {
            alert('Please select an answer.')
            return
        } 
        else {
            setSubmitted(true)
            if (selected !== null) {
                user_answer = currQuestion.choices[selected]
            }
        }

        // Check if answer is correct
        // Display correct/incorrect
        // socket event to server
        console.log(`email: ${auth.email}, question_id: ${currQuestion.question_id}, user_answer: ${user_answer}, time left: ${timer}, max time: ${maxTime}`);
        socket.emit('check_answer', { 
            "email": auth.email,  
            "question_id": currQuestion.question_id, 
            "user_answer": user_answer, 
            "question_index": questionIndex,
            "time_left": timer,
            "max_time": maxTime
        })
        console.log('emitted');
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

    function getProgressBarColor(progress) {     
        if (progress > 66) {
            return 'success'
        }
        else if (progress > 33) {
            return 'warning'
        }
        else {
            return 'danger'
        }
    }

    // useEffect to handle question timer
    useEffect(() => {
        const interval = setInterval(() => {

            if (timer >= 0)
            {   
                // Pause timer if question is submitted
                if (!submitted) {
                    setTimer((prevTime) => prevTime - 1);
                }
            } else {
                clearInterval(interval);
                handleSubmit()
            }
        }, 1000);

        return () => clearInterval(interval); // Cleanup on component unmount
    }, [timer])

    // Display correct/incorrect icons after question is submitted
    function resultIcon(index) {
        if (correct !== null) {
            console.log("result Icon", correct, index, selected);
            if (index === correct) {
                return <i className="bi bi-check-circle-fill position-absolute end-0 me-5"></i>
            }
            else if (index === selected) {
                return <i className="bi bi-x-circle-fill position-absolute end-0 me-5"></i>
            }
        }
    }

    return (
        // If no questions, redirect to setup page. Either error or user tried to access quiz page directly.
        (questions.length === 0)
        ? <Navigate to='/singleplayer/setup' replace />
          // Question card, with prompt and choices.
        : <Card className='d-flex flex-row justify-content-center col-11 col-lg-8 slide-down'>
            <Container>
                <Row className='d-flex flex-row justify-content-end align-items-center mx-3 mt-3'>
                    <Col xs="auto">Time: {timer > 0 ? timer : 0}s</Col>
                </Row>
                <Row className='d-flex flex-row justify-content-center mx-3 mt-3'>
                    <Col >
                        <ProgressBar 
                            now={timer} 
                            max={maxTime} 
                            animated 
                            variant={getProgressBarColor((timer/maxTime)*100)}
                        /> 
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