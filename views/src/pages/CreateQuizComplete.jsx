import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'

import { useLocation, useNavigate } from 'react-router-dom'

export default function CreateQuizComplete() {
        const location = useLocation()
        const questions = location.state ?? []
        const navigate = useNavigate()
        
        return  (
            <Card className='d-flex flex-row justify-content-center w-50 shadow-sm mt-3'>
                <h1 className='text-center'>Quiz Created!</h1>
                <Button variant="primary" onClick={() => navigate('/quiz/play', {state: {questions}})}>Play Quiz</Button>
            </Card>
        ) 
}