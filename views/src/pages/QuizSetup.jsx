import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Loading from '../components/Loading'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { categories } from '../constants'
import useAxios from '../hooks/useAxios'

/*
    The QuizSetup component is a form that allows the user to select the 
    number of questions, the category, the difficulty, and the type of questions they want to answer.
    The form is submitted to the server to get the questions and then the user is navigated to Quiz.jsx page.
*/

export default function QuizSetup() {
    const axios = useAxios()
    const navigate = useNavigate()

    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()
        
        try {
            setLoading(true)
            const response = await axios.post(
                '/quiz', 
                {
                    "amount": e.target.amount.value,
                    "category": e.target.category.value,
                    "difficulty": e.target.difficulty.value,
                    "type": e.target.type.value
                },
            )
            setLoading(false)
            
            console.log(response.data)
            console.log(response.data.length)    
            // navigate to the quiz page with the questions
            navigate('/singleplayer/play', {state: {questions: response.data}})

        } catch (error) {
            setLoading(false)
            console.error(error)
        }        

    }

    if (loading) {
        return <Loading />
    }

    return (
        // Form to select the number of questions, category, difficulty, and type of questions
        <Card className='d-flex flex-row justify-content-center col-11 col-lg-4 shadow-sm mt-3 slide-down'>
            <Form className='p-3 w-100' onSubmit={handleSubmit}>

                <Form.Group className='mb-3' controlId='amount'>
                    <Form.Label>Choose the number of questions</Form.Label>
                    <Form.Control type="number" placeholder='10' defaultValue={10} min='1' max='50' required/>
                </Form.Group>

                <Form.Group className='mb-3' controlId='category'>
                    <Form.Label>Choose the category</Form.Label>
                    <Form.Select>
                        {categories.map(([value, label]) => {
                            return <option key={label} value={value}>{label}</option>
                        })}
                    </Form.Select>
                </Form.Group>

                <Form.Group className='mb-3' controlId='difficulty'>
                    <Form.Label>Choose the difficulty</Form.Label>
                    <Form.Select>
                        <option value=''>Any Difficulty</option>
                        <option value='easy'>Easy</option>
                        <option value='medium'>Medium</option>
                        <option value='hard'>Hard</option>
                    </Form.Select>
                </Form.Group>

                <Form.Group className='mb-3' controlId='type'>
                    <Form.Label>Choose the type</Form.Label>
                    <Form.Select>
                        <option value=''>Any Type</option>
                        <option value='multiple'>Multiple Choice</option>
                        <option value='boolean'>True / False</option>
                    </Form.Select>
                </Form.Group>
                
                <Button variant="primary" type="submit">Start Quiz</Button>
            </Form>
    </Card>
    )
}