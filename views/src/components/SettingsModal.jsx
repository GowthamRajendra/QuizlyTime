import Modal from "react-bootstrap/Modal";
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'

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
                    
                    <Button variant="primary" type="submit">Start Quiz</Button>
                </Form>
            </Card>
        </Modal>
    )
}

export default SettingsModal