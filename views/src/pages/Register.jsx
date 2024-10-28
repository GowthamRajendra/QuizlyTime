import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'

function Register() {
    return (
        <Card className='d-flex flex-row justify-content-center w-50 shadow-sm mt-3'>
            <Form className='pt-3 pb-3 w-75'>
                <Form.Group className='mb-3' controlId='formEmail'>
                    <Form.Label>Email address</Form.Label>
                    <Form.Control type="email" placeholder='abc@email.com'/>
                </Form.Group>

                <Form.Group className='mb-3' controlId='formUsername'>
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="username" placeholder='Username'/>
                </Form.Group>

                <Form.Group className='mb-3' controlId='formPassword'>
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder='Password'/>
                </Form.Group>
                
                <Button variant="primary" type="submit">Register</Button>
                <hr />
                <Form.Text>Already have an account? <a href='/login'>Sign In</a></Form.Text>
            </Form>
        </Card>
    )
}

export default Register