import { io } from 'socket.io-client'
import { createContext, useState, useEffect } from 'react'

const MultiplayerSocketContext = createContext();

export const MultiplayerSocketProvider = ({children}) => {
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const newSocket = io(`${import.meta.env.VITE_SOCKET_URL || 'http://localhost:5000'}/multiplayer`,
            {
                transports:['websocket'],
                withCredentials: true
            }
        )
        setSocket(newSocket)
        
        newSocket.on('connect', () => {
            console.log("CONNECTED")
        })

        newSocket.on('no_namespace', () => {
            console.log("TRIED MULTIPLAYER BUT DID NOT CONNECT TO NAMESPACE")
        })
        
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