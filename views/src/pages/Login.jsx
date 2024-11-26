import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import Card from 'react-bootstrap/Card'
import { useState} from 'react'
import useAxios from '../hooks/useAxios'
import { useNavigate, useLocation, Navigate } from 'react-router-dom'
import useAuth from '../hooks/useAuth'
import { Link } from 'react-router-dom'

function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const axios = useAxios()
    const { auth, setAuth } = useAuth()

    const navigate = useNavigate()
    const location = useLocation()
    const to = location.state?.to || '/'

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

            setAuth({"email": email2, "username": username})
            setEmail('')
            setPassword('')
            
            // navigate to the page the user was trying to access before being redirected to the login page
            // replace the current history entry so the user cannot go back to the login page
            console.log(`Navigating to ${to}`)
            navigate(to, {replace: true})
        } catch (err) {
            if (!err?.response) {
                console.error("No error response")
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
        auth
        ? <Navigate to={to} replace />
        : <Card className='d-flex flex-row justify-content-center w-50 shadow-sm mt-3'>
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
                <Form.Text>Don't have an account? <Link to="/register">Sign Up</Link></Form.Text>
            </Form>
        </Card>
    )
}

export default Login