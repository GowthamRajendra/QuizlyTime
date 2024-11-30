import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { useState, useEffect } from 'react'
import { useLocation, useNavigate, Navigate } from 'react-router-dom'

import useAxios from '../hooks/useAxios'

// Page for user to create the questions for custom quiz

export default function CreateQuiz() {
    const axios = useAxios()
    const navigate = useNavigate()

    // Get quiz details from setup page
    const location = useLocation()
    const quizDetails = location.state ?? {title: 'My Quiz', questions: [], quiz_id: null}

    const [questions, setQuestions] = useState(quizDetails.questions)

    const [questionIndex, setQuestionIndex] = useState(0)
    const currQuestion = questions[questionIndex]

    // when user has finished creating all questions
    const [isSubmited, setIsSubmited] = useState(false)
    
    // for radio buttons
    const [isCategorySelect, setIsCategorySelect] = useState(quizDetails.questions[0].categorySelect) // true = select, false = create
    const [isMultiple, setIsMultiple] = useState(quizDetails.questions[0].multiple)  // true = mc, false = t/f

    // current values for category, difficulty, true/false
    // used to set default values in the select elements  
    // because it seems defaultValue attribute does not work with dynamic values
    const [currentDifficulty, setCurrentDifficulty] = useState('easy')
    const [currentCategory, setCurrentCategory] = useState('9')
    const [currentTrueFalse, setCurrentTrueFalse] = useState('True')
    
    const handleNext = (e) => {
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
            question_id: currQuestion.question_id ?? null,
            prompt,
            categorySelect: isCategorySelect,
            category,
            difficulty,
            multiple: isMultiple,
            choices,
            answer
        }
        
        // update questions array
        const newQuestions = [...questions] // shallow copy
        newQuestions[questionIndex] = newQuestion
        setQuestions(newQuestions)

        // if not last question, increment index 
        // else, set isSubmited to true so we can navigate to the next page
        if (questionIndex < questions.length - 1) {
            setQuestionIndex(questionIndex + 1)
        }  else {
            setIsSubmited(true)
        }
    }

     // Navigate back to the previous question
     const handlePrevious = () => {
        // clear current form
        document.getElementById('question-form').reset()

        setQuestionIndex((prev) => Math.max(prev - 1, 0))
    };

    const saveNewCustomQuiz = async (questionsFormatted) => {
        try {
            const response = await axios.post('/save-custom-quiz', {
                title: quizDetails.title,
                questions: questionsFormatted
            })
            console.log(response.data)
            navigate('/quiz/create/complete', {state: {questions: response.data}})
        } catch (error) {
            console.error(error)
        }
    }

    const saveEdittedCustomQuiz = async (questionsFormatted) => {
        try {
            const response = await axios.put(`/edit-custom-quiz`, {
                title: quizDetails.title,
                questions: questionsFormatted,
                quiz_id: quizDetails.quiz_id
            })
            console.log(response.data)
            navigate('/quiz/create/complete', {state: {questions: response.data}})
        } catch (error) {
            console.error(error)
        }
    }

    useEffect(() => {
        if (isSubmited) {
            let questionsFormatted = questions.map((question, index) => {
                return {
                    id: question.question_id ?? null,
                    question: question.prompt,    
                    category: question.category,
                    difficulty: question.difficulty,
                    type: question.multiple ? 'multiple' : 'boolean',
                    incorrect_answers: question.choices,
                    correct_answer: question.answer
                }
            })

            // if quiz_id is not null, we are editing an existing quiz
            console.log("quiz_id", quizDetails.quiz_id)
            if (quizDetails.quiz_id !== null) {
                saveEdittedCustomQuiz(questionsFormatted)
            } else {
                saveNewCustomQuiz(questionsFormatted)
            }
        }

        // set current values for category, difficulty, true/false
        setIsCategorySelect(questions[questionIndex].categorySelect)
        setIsMultiple(questions[questionIndex].multiple)
        setCurrentCategory(questions[questionIndex].category)
        setCurrentDifficulty(questions[questionIndex].difficulty)
        setCurrentTrueFalse(questions[questionIndex].answer)

    }, [questionIndex, questions, isSubmited])

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
                        {/* did not implement random questions feature. leaving it for potential future use/}
                        {/* <Button variant='info' size='sm'>Get Random Question</Button> */}
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
                            Back
                        </Button>
                        <Button variant="primary" type="submit">
                            {questionIndex < questions.length - 1 ? 'Next' : 'Save'}
                        </Button>
                    </div>
                </Form>
            </Card.Body>
        </Card>
    )
}
