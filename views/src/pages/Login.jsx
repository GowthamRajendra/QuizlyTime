import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import Card from 'react-bootstrap/Card'

function Login() {
    return (
        <Card className='d-flex flex-row justify-content-center w-50 shadow-sm mt-3'>
            <Form className='pt-3 pb-3 w-75'>
                <Form.Group className='mb-3' controlId='formEmail'>
                    <Form.Label>Email address</Form.Label>
                    <Form.Control type="email" placeholder='abc@email.com'/>
                </Form.Group>

                <Form.Group className='mb-3' controlId='formPassword'>
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder='Password'/>
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