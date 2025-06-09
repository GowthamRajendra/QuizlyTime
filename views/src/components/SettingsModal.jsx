import Modal from "react-bootstrap/Modal";
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import { categories } from "../constants";

// Settings popup for the multiplayer lobby page

function SettingsModal({show, handleSubmit}) {

    return (
        // Form to select the number of questions, category, difficulty, and type of questions
        <Modal centered show={show}>
            <Card className='d-flex flex-row justify-content-center card'>
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
                    
                    <Button variant="primary" type="submit">Apply</Button>
                </Form>
            </Card>
        </Modal>
    )
}

export default SettingsModal