import { useState } from 'react'
import './App.css'
import Button from 'react-bootstrap/Button'
import 'bootstrap/dist/css/bootstrap.min.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <Button onClick={() => setCount((count) => count + 1)}>
          Clicked {count} times
        </Button>
      </div>
    </>
  )
}

export default App
