import { io } from 'socket.io-client'
import { createContext, useState, useEffect } from 'react'

const MultiplayerSocketContext = createContext();

export const MultiplayerSocketProvider = ({children}) => {
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const newSocket = io('localhost:5000/multiplayer')
        setSocket(newSocket)
        
        return () => {
            newSocket.disconnect()
        }
    }, [])

    return (
        <MultiplayerSocketContext.Provider value={socket}>
            {children}
        </MultiplayerSocketContext.Provider>
    )
}

export default MultiplayerSocketContext