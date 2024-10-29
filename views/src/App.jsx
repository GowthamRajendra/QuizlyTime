import { useState } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css'
import Login from './pages/Login'
import Register from './pages/Register'
import MyNavbar from './components/MyNavbar'
import Quiz from './pages/Quiz'
import { Routes, Route } from 'react-router-dom'
import useAuth from './hooks/useAuth'

function App() {
  const { auth } = useAuth()

  return (
    <>
      <MyNavbar />
      <div className='d-flex justify-content-center'>
        <Routes>
          <Route path='/' element={!auth ? <div>Home</div> : <div>Welcome {auth.username}!</div> } />
          <Route path='/login' element={<Login />} />
          <Route path='/register' element={<Register />} />
          <Route path='/quiz' element={<Quiz/>}/>
        </Routes>
      </div>
    </>
  )
}

export default App
