import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { useEffect } from 'react'
import { useState } from 'react'

import io from 'socket.io-client'

import axios from '../api/axios'

import QuizQuestion from '../components/QuizQuestion'

const socket = io('http://localhost:5000')

export default function Quiz(questions) {

    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
    const [isAnswered, setIsAnswered] = useState(false)

    socket.on("connect", () => {
        console.log(socket.connected); // true
      });


    useEffect(() => {
        
        socket.on('answer_checked', (data) => {
            console.log('answer checked');
            console.log(data);
        })        

        // Clean up. Remove the event listener when the component is unmounted
        return () => {
            // remove the event listener
            // prevent memory leaks and unexpected behavior
            socket.off('answer_checked')
        }
    }, [])

    const handleNextQuestion = async () => {


        socket.emit('check_answer', { "question_id": "6722d8fc1808cd2c7fbdfcde", "user_answer": "True" })
        console.log('emitted');
    }


    return (
        <Card className='d-flex flex-row justify-content-center w-50 shadow-sm mt-3'>
            {/* <QuizQuestion question={questions[currentQuestionIndex]} isAnswered={isAnswered} setIsAnswered={setIsAnswered}/> */}
            <Container>
                <Row className='d-flex flex-row justify-content-between'>
                    <Col xs="auto">Question {currentQuestionIndex + 1} of {questions.length}</Col>
                    <Col xs="auto"><Button variant='primary' onClick={handleNextQuestion}>Next Question</Button></Col>
                </Row>
            </Container>
        </Card>
    )
}
