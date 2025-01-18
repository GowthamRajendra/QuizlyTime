import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Alert from 'react-bootstrap/Alert'
import Loading from '../components/Loading'

import { useState } from 'react'
import useAxios from '../hooks/useAxios'
import useAuth from '../hooks/useAuth'
import { useNavigate, Navigate } from 'react-router-dom'
import { Link } from 'react-router-dom'

function Register() {
    // user inputs
    const [email, setEmail] = useState('')
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    // popup alert
    const [message, setMessage] = useState('') // e.g. "Email already in use"
    const [variant, setVariant] = useState('') // e.g. "danger"

    const [loading, setLoading] = useState(false)

    const axios = useAxios()

    const { auth } = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            setLoading(true)
            const response = await axios.post(
                '/register',
                {"email": email, "username": username, "password": password},
            )
            setLoading(false)

            console.log(JSON.stringify(response?.data))
            setEmail('')
            setUsername('')
            setPassword('')

            navigate('/login', {state: {message: 'Registration successful. Please login.', variant: 'success'}})
        } catch (err) {
            setLoading(false)
            if (!err?.response) {
                console.error("No response")
                setMessage('Network error. Try again later.')
                setVariant('danger')
            }
            else if (err.response) {
                console.error(err.response.data.message)
                setMessage(err.response.data.message)
                setVariant('danger')
            }
            else {
                console.error(err)
                setMessage('Unexpected error. Try again later.')
                setVariant('danger')
            }
        }
    }

    if (loading) {
        return <Loading />  
    }

    return (
        auth
        ? <Navigate to='/' replace />
        : <Card className='d-flex flex-row justify-content-center col-11 col-lg-4 shadow-sm mt-3'>
            <Form className='w-100 p-3' onSubmit={handleSubmit}>
                {
                    (message == '')
                    ? null
                    : <Alert variant={variant} dismissible>{message}</Alert>
                }
                <Form.Group className='mb-3' controlId='formEmail'>
                    <Form.Label>Email address</Form.Label>
                    <Form.Control 
                        type="email" 
                        placeholder='abc@email.com, use a fake email!' 
                        onChange={(e) => setEmail(e.target.value)} 
                        value={email}
                    />
                </Form.Group>

                <Form.Group className='mb-3' controlId='formUsername'>
                    <Form.Label>Username</Form.Label>
                    <Form.Control 
                        type="username" 
                        placeholder='Username' 
                        onChange={(e) => setUsername(e.target.value)} 
                        value={username}
                    />
                </Form.Group>

                <Form.Group className='mb-3' controlId='formPassword'>
                    <Form.Label>Password</Form.Label>
                    <Form.Control 
                        type="password" 
                        placeholder='Password' 
                        onChange={(e) => setPassword(e.target.value)} 
                        value={password}
                    />
                </Form.Group>
                
                <Button id="registerButton" variant="primary" type="submit">Register</Button>
                <hr />
                <Form.Text>Already have an account? <Link to="/login">Login</Link></Form.Text>
            </Form>
        </Card>
    )
}

export default Register