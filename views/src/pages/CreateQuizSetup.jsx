import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'

import { useNavigate } from 'react-router-dom'

export default function CreateQuizSetup() { 

    const navigate = useNavigate()

    const handleContinue = (e) => {
        e.preventDefault()

        const title = e.target.title.value
        const amount = e.target.amount.value

        e.target.reset() // clear form

        // create questions array with default values
        const newQuestions = Array.from({length: amount}, (_, i) => ({
            prompt: '',
            categorySelect: true,
            category: '',
            difficulty: 'easy',
            multiple: true,
            choices: [],
            answer: ''
        }))


        // navigate to questions creation
        navigate('/quiz/create/questions', {state: {title, questions: newQuestions, quiz_id: null}})
    }

    return  (
        <Card className='d-flex flex-row justify-content-center col-11 col-lg-4 shadow-sm mt-3'>
            <Form className='p-3 w-100' onSubmit={handleContinue}>
                <Form.Group className='mb-3' controlId='title'>
                    <Form.Label>Choose a title for your quiz</Form.Label>
                    <Form.Control type="text" placeholder='My Quiz' required maxLength={37}/>
                </Form.Group>

                <Form.Group className='mb-3' controlId='amount'>
                    <Form.Label>Choose the number of questions</Form.Label>
                    <Form.Control type="number" placeholder='10' defaultValue={10} min='1' max='50' required/>
                </Form.Group>

                <Button variant="primary" type="submit">Continue</Button>
            </Form>
        </Card>
    ) 
}