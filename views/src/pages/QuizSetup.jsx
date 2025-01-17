import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Loading from '../components/Loading'

import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

import useAxios from '../hooks/useAxios'

/*
    The QuizSetup component is a form that allows the user to select the 
    number of questions, the category, the difficulty, and the type of questions they want to answer.
    The form is submitted to the server to get the questions and then the user is navigated to Quiz.jsx page.
*/

const categories = [
    ['', "Any Category"],
    ['9', "General Knowledge"],
    ['10', "Books"],
    ['11', "Film"],
    ['12', "Music"],
    ['13', "Musicals & Theatres"],
    ['14', "Television"],
    ['15', "Video Games"],
    ['16', "Board Games"],
    ['17', "Science & Nature"],
    ['18', "Computers"],
    ['19', "Mathematics"],
    ['20', "Mythology"],
    ['21', "Sports"],
    ['22', "Geography"],
    ['23', "History"],
    ['24', "Politics"],
    ['25', "Art"],
    ['26', "Celebrities"],
    ['27', "Animals"],
    ['28', "Vehicles"],
    ['29', "Comics"],
    ['30', "Gadgets"],
    ['31', "Japanese Anime & Manga"],
    ['32', "Cartoon & Animations"]
];

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
            navigate('/quiz/play', {state: {questions: response.data}})

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
        <Card className='d-flex flex-row justify-content-center w-75 shadow-sm mt-3'>
            <Form className='p-3 w-100' onSubmit={handleSubmit}>

                <Form.Group className='mb-3' controlId='amount'>
                    <Form.Label>Choose the number of questions</Form.Label>
                    <Form.Control type="number" placeholder='10' defaultValue={10} min='1' max='50' required/>
                </Form.Group>

                <Form.Group className='mb-3' controlId='category'>
                    <Form.Label>Choose the category</Form.Label>
                    <Form.Select>
                        {categories.map((category) => {
                            return <option value={category[0]}>{category[1]}</option>
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