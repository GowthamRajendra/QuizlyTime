import { useEffect, useState, useRef } from 'react'
import useMultiplayerSocket from '../../hooks/useMultiplayerSocket'
import { useNavigate, useLocation } from 'react-router-dom'
import SettingsModal from '../../components/SettingsModal'

function Lobby() {
    const socket = useMultiplayerSocket()
    const navigate = useNavigate()
    const location = useLocation()
    // check if user left page via starting game or main page
    // important for leaving the room on the server side if it was an
    // improper leave (leaving page without pressing 'leave game')
    const improperLeave = useRef(true)
    
    const [showSettings, setShowSettings] = useState(false)
    const [messageVal, setMessageVal] = useState('')
    const [roomCode, setRoomCode] = useState(location.state?.code ?? '')
    const [users, setUsers] = useState(location.state?.users ?? [])
    const [messages, setMessages] = useState([])

    // quiz settings
    const [qAmount, setQAmount] = useState(10)
    const [qCategory, setQCategory] = useState('')
    const [qDifficulty, setQDifficulty] = useState('')
    const [qType, setQType] = useState('')

    

    // initialize all relevant socket stuff for this page.
    useEffect(() => {
        
        // functions for handling the socket endpoints
        const handlePlayerJoined = ({names}) => {
            setUsers(names)
        }
        const handlePlayerMessage = ({message, name}) => {
            console.log(`${name}: ${message}`)
            setMessages(prevMessages => [...prevMessages, `${name}: ${message}`])
        }
        const handlePlayerLeft = ({name}) => {
            setUsers(prevUsers => prevUsers.filter(user => user !== name))
        }
        const handleStartGame = ({questions}) => {
            console.log(questions)
            navigate('/multiplayer/play', {state: {questions: questions}})
        }
        const handleLeaveRoom = () => {
            setUsers([])
            setMessages([])
            setRoomCode('')
            navigate('/multiplayer')
        }
        
        // get list of players when you enter lobby
        socket.emit('current_players') 

        // setup listeners
        socket.on('player_joined', handlePlayerJoined)
        socket.on('player_message', handlePlayerMessage)
        socket.on('player_left', handlePlayerLeft)
        socket.on('start_game', handleStartGame)
        socket.on('leave_room_successful', handleLeaveRoom)

        console.log(socket.listeners('start_game'))
        
        // cleanup endpoints so duplicates dont build up everytime you
        // return to the lobby page.
        return () => {
            socket.off('player_joined', handlePlayerJoined)
            socket.off('player_message', handlePlayerMessage)
            socket.off('player_left', handlePlayerLeft)
            socket.off('start_game', handleStartGame)
            socket.off('leave_room_successful', handleLeaveRoom)
        }
    }, [])

    // send quiz settings and begin multiplayer quiz for all connected players
    const startGame = () => {

        console.log("sending settings")

        socket.emit('start_game', {
            "amount": `${qAmount}`,
            "type": qType,
            "difficulty": qDifficulty,
            "category": qCategory
        })
    }

    // store the settings for the quiz questions
    const handleSettings = (e) => {
        e.preventDefault()
        setQAmount(e.target.amount.value)
        setQCategory(e.target.category.value)
        setQDifficulty(e.target.difficulty.value)
        setQType(e.target.type.value)

        console.log(e.target.amount.value, e.target.category.value, e.target.difficulty.value, e.target.type.value)
        setShowSettings(!showSettings)
    }

    const leaveRoom = () => {
        socket.emit('leave_room')
    }

    const sendMessage = () => {
        socket.emit('player_message', {'message': messageVal})
    }

    return <div>
        <SettingsModal show={showSettings} handleSubmit={handleSettings}></SettingsModal>
        <h2>LOBBY: {roomCode}</h2>
        <button onClick={() => startGame()}>Start Game</button>
        <button onClick={() => setShowSettings(!showSettings)}>Game Settings</button>
        <button onClick={() => leaveRoom()}>Leave Room</button>
        <div>
            {users.map((user, idx) => (
                <li key={idx}>{user}</li>
            ))}
        </div>
        <button onClick={() => sendMessage()}>Send Message</button>
        <input type="text" value={messageVal} onChange={(e) => {setMessageVal(e.target.value)}}/>
        <div>
            {messages.map((message, idx) => (
                <ul key={idx}>{message}</ul>
            ))}
        </div>
    </div>
}

export default Lobby