import { useLocation, useNavigate } from "react-router-dom"
import useMultiplayerSocket from '../../hooks/useMultiplayerSocket';
import { useEffect } from "react";

function MultiplayerResults() {
    const location = useLocation()
    const navigate = useNavigate()
    const results = location.state?.results ?? []
    const socket = useMultiplayerSocket()

    useEffect(() => {
        return () => {
            socket.emit('leave_room')
        }
    }, [])

    return <div>
        <ol>
            {results.map(({idx, name, score}) => (
                <li key={idx}>{name}: {score}</li>
            ))}
        </ol>
        {/* <button onClick={() => navigate('/multiplayer')}>Play Again</button> */}
        <button onClick={() => navigate('/play')}>Leave</button>
    </div>
}

export default MultiplayerResults