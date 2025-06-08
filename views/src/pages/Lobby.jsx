import { useEffect, useState } from 'react'
import useMultiplayerSocket from '../hooks/useMultiplayerSocket'
import { useNavigate, useLocation } from 'react-router-dom'

function Lobby() {
    const socket = useMultiplayerSocket()
    const navigate = useNavigate()
    const location = useLocation()
    
    const [messageVal, setMessageVal] = useState('')
    const [roomCode, setRoomCode] = useState(location.state?.code ?? '')
    const [users, setUsers] = useState(location.state?.users ?? [])
    const [messages, setMessages] = useState([])

    useEffect(() => {
        // get list of players when you enter lobby
        socket.emit('current_players') 

        socket.on('player_joined', ({names}) => {
            setUsers(names)
        })

        socket.on('player_message', ({message, name}) => {
            console.log(`${name}: ${message}`)
            setMessages(prevMessages => [...prevMessages, `${name}: ${message}`])
        })

        socket.on('player_left', ({name}) => {
            setUsers(prevUsers => prevUsers.filter(user => user !== name))
        })

        socket.on('leave_room_successful', () => {
            setUsers([])
            setMessages([])
            setRoomCode('')
            navigate('/multiplayer')
        })
    }, [])

    const leaveRoom = () => {
        socket.emit('leave_room')
    }

    const sendMessage = () => {
        socket.emit('player_message', {'message': messageVal})
    }

    return <div>
        <h2>LOBBY: {roomCode}</h2>
        <button>Start Game</button>
        <button>Game Settings</button>
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