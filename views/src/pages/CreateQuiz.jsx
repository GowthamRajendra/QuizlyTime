import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { useState } from 'react'
import { useLocation, useNavigate, Navigate } from 'react-router-dom'

import useAxios from '../hooks/useAxios'

// Page for user to create a custom quiz

export default function CreateQuiz() {
    const axios = useAxios()
    const navigate = useNavigate()

    // Get quiz details from setup page
    const location = useLocation()
    const quizDetails = location.state ?? {title: 'My Quiz', questions: []}

    const [questions, setQuestions] = useState(quizDetails.questions)

    const [questionIndex, setQuestionIndex] = useState(0)
    const currQuestion = questions[questionIndex]
    
    // for radio buttons
    const [isCategorySelect, setIsCategorySelect] = useState(true) // true = select, false = create
    const [isMultiple, setIsMultiple] = useState(true) // true = mc, false = t/f

    // current values for category, difficulty, true/false
    // used to set default values in the select elements  
    // because it seems defaultValue does not work with dynamic values
    const [currentDifficulty, setCurrentDifficulty] = useState('easy')
    const [currentCategory, setCurrentCategory] = useState('9')
    const [currentTrueFalse, setCurrentTrueFalse] = useState('True')
    
    const handleNext = async (e) => {
        e.preventDefault()

        const prompt = e.target.prompt.value
        const category = e.target.category.value
        const difficulty = e.target.difficulty.value
        const answer = e.target.answer.value

        let choices = []
        if (isMultiple) {
            choices = [e.target.choices[0].value, e.target.choices[1].value, e.target.choices[2].value]
        } else {
            choices = answer === 'True' ? ['False'] : ['True']
        }

        e.target.reset() // clear form

        const newQuestion = {
            prompt,
            categorySelect: isCategorySelect,
            category,
            difficulty,
            multiple: isMultiple,
            choices,
            answer
        }
        
        // update questions array
        const newQuestions = [...questions]
        newQuestions[questionIndex] = newQuestion
        setQuestions(newQuestions)

        console.log(questions);

        // if not last question, increment index 
        if (questionIndex < questions.length - 1) {
            setQuestionIndex(questionIndex + 1)
            setIsCategorySelect(questions[questionIndex + 1].categorySelect)
            setIsMultiple(questions[questionIndex + 1].multiple)
            setCurrentCategory(questions[questionIndex + 1].category)
            setCurrentDifficulty(questions[questionIndex + 1].difficulty)
            setCurrentTrueFalse(questions[questionIndex + 1].answer)
        } else {
            // navigate to quiz page
            // navigate('/quiz/play', {state: {questions: questions}})
          
            let questionsFormatted = questions.map((question, index) => {
                return {
                    question: question.prompt,    
                    category: question.category,
                    difficulty: question.difficulty,
                    type: question.multiple ? 'multiple' : 'boolean',
                    incorrect_answers: question.choices,
                    correct_answer: question.answer
                }
            })

            console.log(questionsFormatted);

            // try {
            //     const response = await axios.post(
            //         '/custom-quiz', 
            //         {
            //             "title": quizDetails.title,
            //             "questions": questionsFormatted
            //         },
            //     )
                
            //     console.log(response.data)
            //     navigate('/quiz/play', {state: {quiz: response.data}})
            // } catch (error) {
            //     console.error(error)
            // }  

            axios.post('/custom-quiz', {
                title: quizDetails.title,
                questions: questionsFormatted
            }).then(response => {
                console.log(response.data)
                navigate('/quiz/play', {state: {quiz: response.data}})
            }).catch(error => {
                console.error(error)
            })
        }
    }

     // Navigate back to the previous question
     const handlePrevious = () => {

        // clear current form
        document.getElementById('question-form').reset()

        console.log(questions);

        setQuestionIndex((prev) => Math.max(prev - 1, 0))
        
        // set current values for category, difficulty, true/false
        // setState for question index is async, so this is to ensure the correct values are set

        let index = Math.max(questionIndex - 1, 0)

        setIsCategorySelect(questions[index].categorySelect)
        setIsMultiple(questions[index].multiple)
        setCurrentCategory(questions[index].category)
        setCurrentDifficulty(questions[index].difficulty)
        setCurrentTrueFalse(questions[index].answer)
    };

    return (
        // if no questions, redirect to setup page
        (questions.length === 0) 
        ? <Navigate to='/quiz/create/setup' /> 
        : <Card className='d-flex flex-column justify-content-center w-50 shadow-sm mt-3'>
            <Card.Header className='mb-1'> 
                <Row className='d-flex flex-row justify-content-between'>
                    <Col className='d-flex flex-row justify-content-start align-items-center'>
                        Question {questionIndex + 1} of {questions.length} 
                    </Col>
                    <Col className='d-flex flex-row justify-content-end align-items-center'>
                        <Button variant='info' size='sm'>Get Random Question</Button>
                    </Col>
                </Row>
            </Card.Header>
            <Card.Body style={{marginLeft: '1rem', marginRight: '1rem'}}>
                <Form onSubmit={handleNext} id='question-form'>
                    <Form.Group className='mb-3' controlId='prompt'>
                        <Form.Label>Enter Question</Form.Label>
                        <Form.Control type="text" placeholder='What is 1+1?' required defaultValue={currQuestion.prompt}/>
                    </Form.Group>

                    <Row className='d-flex flex-row justify-content-between'>
                        <Col>
                            <Form.Group className="mb-3">
                                <Form.Label>Choose or Create a Category</Form.Label>
                                <br />
                                <Form.Check
                                    inline
                                    label="Choose Category"
                                    name="category-radio"
                                    type='radio'
                                    id='category-select-radio'
                                    checked={isCategorySelect}
                                    onChange={() => setIsCategorySelect(true)}
                                />
                                <Form.Check
                                    inline
                                    label="Create Category"
                                    name="category-radio"
                                    type='radio'
                                    id='category-create-radio'
                                    checked={!isCategorySelect}
                                    onChange={() => setIsCategorySelect(false)}
                                />
                            </Form.Group>
                        </Col>
                        <Col>
                        {isCategorySelect ? 
                            <Form.Group className='mb-3' controlId='category'>
                                <Form.Label>Choose Category</Form.Label>
                                <Form.Select 
                                        value={isCategorySelect ? currentCategory : 'General Knowledge'} 
                                        onChange={(e) => setCurrentCategory(e.target.value)}>
                                    <option value='General Knowledge'>General Knowledge</option>
                                    <option value='Books'>Books</option>
                                    <option value='Film'>Film</option>
                                    <option value='Music'>Music</option>
                                    <option value='Musicals & Theatres'>Musicals & Theatres</option>
                                    <option value='Television'>Television</option>
                                    <option value='Video Games'>Video Games</option>
                                    <option value='Board Games'>Board Games</option>
                                    <option value='Science & Nature'>Science & Nature</option>
                                    <option value='Computers'>Computers</option>
                                    <option value='Mathematics'>Mathematics</option>
                                    <option value='Mythology'>Mythology</option>
                                    <option value='Sports'>Sports</option>
                                    <option value='Geography'>Geography</option>
                                    <option value='History'>History</option>
                                    <option value='Politics'>Politics</option>
                                    <option value='Art'>Art</option>
                                    <option value='Celebrities'>Celebrities</option>
                                    <option value='Animals'>Animals</option>
                                    <option value='Vehicles'>Vehicles</option>
                                    <option value='Comics'>Comics</option>
                                    <option value='Gadgets'>Gadgets</option>
                                    <option value='Japanese Anime & Manga'>Japanese Anime & Manga</option>
                                    <option value='Cartoon & Animations'>Cartoon & Animations</option>
                                </Form.Select>
                            </Form.Group>
                            : 
                            <Form.Group className='mb-3' controlId='category'>
                                <Form.Label>Create Category</Form.Label>
                                <Form.Control type="text" placeholder='My Category' required defaultValue={currQuestion.category}/>
                            </Form.Group>
                        }
                        </Col>
                    </Row>
                    
                    <Form.Group className='mb-3' controlId='difficulty'>
                        <Form.Label>Choose The Difficulty</Form.Label>
                        <Form.Select value={currentDifficulty} onChange={(e) => setCurrentDifficulty(e.target.value)}>
                            <option value='easy'>Easy</option>
                            <option value='medium'>Medium</option>
                            <option value='hard'>Hard</option>
                        </Form.Select>
                    </Form.Group>
                    
                    <Row className='d-flex flex-row justify-content-between'>
                        <Col>
                            <Form.Group className="mb-3">
                                <Form.Label>Multiple Choice or True/False</Form.Label>
                                <br />
                                <Form.Check
                                    inline
                                    label="Multiple Choice"
                                    name="type-radio"
                                    type='radio'
                                    id='multiple-choice-radio'
                                    checked={isMultiple}
                                    onChange={() => setIsMultiple(true)}
                                />
                                <Form.Check
                                    inline
                                    label="True/False"
                                    name="type-radio"
                                    type='radio'
                                    id='true-false-radio'
                                    checked={!isMultiple}
                                    onChange={() => setIsMultiple(false)}
                                />
                            </Form.Group>
                        </Col>  
                        <Col>
                            {isMultiple ?
                                <Form.Group className='mb-3' controlId='answer'>
                                    <Form.Label>Enter Correct Answer</Form.Label>
                                    <Form.Control type="text" placeholder='Answer' required defaultValue={currQuestion.answer}/>
                                </Form.Group> 
                                : 
                                <Form.Group className='mb-3' controlId='answer'>
                                        <Form.Label>Choose the Correct Answer</Form.Label>
                                        <Form.Select value={currentTrueFalse} onChange={(e) => setCurrentTrueFalse(e.target.value)}>
                                            <option value='True'>True</option>
                                            <option value='False'>False</option>
                                        </Form.Select>
                                </Form.Group>
                            }   
                        </Col>
                    </Row>

                    {isMultiple ?
                        <Form.Group className='mb-3' controlId='choices'>
                            <Form.Label>Enter Incorrect Choices</Form.Label>
                            <Form.Control className='mb-1' type="text" placeholder='Choice 1' required defaultValue={currQuestion.choices[0]}/>
                            <Form.Control className='mb-1' type="text" placeholder='Choice 2' required defaultValue={currQuestion.choices[1]}/>
                            <Form.Control type="text" placeholder='Choice 3' required defaultValue={currQuestion.choices[2]}/>
                        </Form.Group> : null
                    }   
                    
                    <div className='d-flex justify-content-between'>
                        <Button variant="primary" type="button" onClick={handlePrevious} disabled={questionIndex === 0}>
                            Previous
                        </Button>
                        <Button variant="primary" type="submit">
                            {questionIndex < questions.length - 1 ? 'Next' : 'Finish'}
                        </Button>
                    </div>
                </Form>
            </Card.Body>
        </Card>
    )
}
