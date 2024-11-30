import 'bootstrap/dist/css/bootstrap.min.css'
import Home from './pages/Home'
import Profile from './pages/Profile'
import Login from './pages/Login'
import Register from './pages/Register'
import MyNavbar from './components/MyNavbar'
import ChooseQuizType from './pages/ChooseQuizType'
import Quiz from './pages/Quiz'
import QuizSetup from './pages/QuizSetup'
import QuizComplete from './pages/QuizComplete'
import CreateQuizSetup from './pages/CreateQuizSetup'
import CreateQuiz from './pages/CreateQuiz'
import CreateQuizComplete from './pages/CreateQuizComplete'
import QuizSelection from './pages/QuizSelection'
import Protected from './components/Protected'
import { Routes, Route } from 'react-router-dom'
import useAuth from './hooks/useAuth'

function App() {
  const { auth } = useAuth()

  return (
    <>
      <MyNavbar />
      <div className='d-flex justify-content-center'>
        <Routes>
          <Route path='/' element={!auth ? <Home /> : <Profile /> } />
          <Route path='/login' element={<Login />} />
          <Route path='/register' element={<Register />} />
          {/* Protected routes */}
          <Route element={<Protected/>}>
            <Route path='/quiz' element={<ChooseQuizType/>}/>
            <Route path='/quiz/select' element={<QuizSelection/>}/>
            <Route path='/quiz/setup' element={<QuizSetup/>}/>
            <Route path='/quiz/play' element={<Quiz/>}/>
            <Route path='/quiz/results' element={<QuizComplete/>}/>
            <Route path='/quiz/create/setup' element={<CreateQuizSetup/>}/>
            <Route path='/quiz/create/questions' element={<CreateQuiz/>}/>
            <Route path='/quiz/create/complete' element={<CreateQuizComplete/>}/>
          </Route>
        </Routes>
      </div>
    </>
  )
}

export default App
