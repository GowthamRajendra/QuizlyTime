import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import Card from 'react-bootstrap/Card'
import { useState} from 'react'
import axios from '../api/axios'
import { useNavigate } from 'react-router-dom'
import useAuth from '../hooks/useAuth'

function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const { setAuth } = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const response = await axios.post(
                '/login',
                {"email": email, "password": password},
            )
            

            console.log(JSON.stringify(response?.data))
            const email2 = response?.data?.email
            const username = response?.data?.username

            setAuth({email2, username})
            setEmail('')
            setPassword('')

            navigate('/')
        } catch (err) {
            if (!err?.response) {
                console.error("No response")
            }
            else if (err.response) {
                console.error(err.response.data.message)
            }
            else {
                console.error(err)
            }
        }
    }

    return (
        <Card className='d-flex flex-row justify-content-center w-50 shadow-sm mt-3'>
            <Form className='pt-3 pb-3 w-75' onSubmit={handleSubmit}>
                <Form.Group className='mb-3' controlId='formEmail'>
                    <Form.Label>Email address</Form.Label>
                    <Form.Control 
                        type="email" 
                        placeholder='abc@email.com' 
                        onChange={(e) => setEmail(e.target.value)}
                        value={email}
                        required
                    />
                </Form.Group>

                <Form.Group className='mb-3' controlId='formPassword'>
                    <Form.Label>Password</Form.Label>
                    <Form.Control 
                        type="password" 
                        placeholder='Password' 
                        onChange={(e) => setPassword(e.target.value)}
                        value={password}
                        required
                    />
                </Form.Group>

                <Form.Group className='mb-3' controlId='formCheck'>
                    <Form.Check type="checkbox" label="Keep me logged in"/>
                </Form.Group>
                
                <Button variant="primary" type="submit">Login</Button>
                <hr />
                <Form.Text>Don't have an account? <a href='/register'>Sign Up</a></Form.Text>
            </Form>
        </Card>
    )
}

export default Login