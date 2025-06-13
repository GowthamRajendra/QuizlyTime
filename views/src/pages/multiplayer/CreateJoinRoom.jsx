import { useEffect, useState } from 'react'
import io from 'socket.io-client'
import useAuth from '../../hooks/useAuth'
import useMultiplayerSocket from '../../hooks/useMultiplayerSocket'
import { useNavigate } from 'react-router-dom'

function CreateJoinRoom() {
    const { auth } = useAuth()
    const navigate = useNavigate()
    const socket = useMultiplayerSocket()
    const [codeVal, setCodeVal] = useState('')

    useEffect(() => {
        // check if user is already in a room. if so, they will be navigated to the lobby.
        socket.emit('check_for_room')
        
        // store some user information on server side for easier user handling
        socket.emit('register_user', {'email': auth.email, 'name': auth.username})

        const handleRoomCreated = ({code}) => {
            navigate('/multiplayer/lobby', {state: {code: code}})
        }

        socket.on('room_created', handleRoomCreated)

        return () => {
            socket.off('room_created', handleRoomCreated)
        }
    }, [])

    const createRoom = () => {
        socket.emit('create_room')
    }

    const joinRoom = () => {
        socket.emit('join_room', {'code': codeVal})
    }

    return <div>
        <button onClick={() => createRoom()}>Create Room</button>
        <button onClick={() => joinRoom()}>Join Room</button>
        <input type="text" placeholder='Enter a room code' value={codeVal} onChange={(e) => {setCodeVal(e.target.value)}}/>
    </div>
}

export default CreateJoinRoom