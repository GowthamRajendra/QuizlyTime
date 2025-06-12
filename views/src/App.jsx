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
import { Routes, Route} from 'react-router-dom'
import useAuth from './hooks/useAuth'
// import Loading from './components/Loading'
import CreateJoinRoom from './pages/multiplayer/CreateJoinRoom'
import Lobby from './pages/multiplayer/Lobby'
import MultiplayerGame from './pages/multiplayer/MultiplayerGame'
import MultiplayerResults from './pages/multiplayer/MultiplayerResults'
import ChooseGameMode from './pages/ChooseGameMode'

function App() {
  const { auth } = useAuth()

  return (
    <>
      <MyNavbar />
      <div className='container d-flex justify-content-center align-items-center'>
        <Routes>
          <Route path='/' element={!auth ? <Home /> : <Profile /> } />
          <Route path='/login' element={<Login />} />
          <Route path='/register' element={<Register />} />
          {/* Protected routes */}
          <Route element={<Protected/>}>
            <Route path='/play' element={<ChooseGameMode/>} />
            <Route path='/singleplayer' element={<ChooseQuizType/>}/>
            <Route path='/singleplayer/select' element={<QuizSelection/>}/>
            <Route path='/singleplayer/setup' element={<QuizSetup/>}/>
            <Route path='/singleplayer/play' element={<Quiz/>}/>
            <Route path='/singleplayer/results' element={<QuizComplete/>}/>
            <Route path='/quiz/create/setup' element={<CreateQuizSetup/>}/>
            <Route path='/quiz/create/questions' element={<CreateQuiz/>}/>
            <Route path='/quiz/create/complete' element={<CreateQuizComplete/>}/>
            <Route path='/multiplayer' element={<CreateJoinRoom/>}/> 
            <Route path='/multiplayer/lobby' element={<Lobby/>}/>
            <Route path='/multiplayer/play' element={<MultiplayerGame/>}></Route>
            <Route path='/multiplayer/results' element={<MultiplayerResults/>}></Route>
            {/* More page will be here that need the socket connection uninterrupted */}
          </Route>
        </Routes>
      </div>
    </>
  )
}

export default App
