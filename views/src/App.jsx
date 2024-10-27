import { useState } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css'
import Login from './pages/Login'
import Register from './pages/Register'
import MyNavbar from './components/MyNavbar'
import { Routes, Route } from 'react-router-dom'

function App() {
  return (
    <>
      <MyNavbar />
      <div className='d-flex justify-content-center'>
        <Routes>
          <Route path='/' element={<div>Home</div>} />
          <Route path='/login' element={<Login />} />
          <Route path='/register' element={<Register />} />
        </Routes>
      </div>
    </>
  )
}

export default App
