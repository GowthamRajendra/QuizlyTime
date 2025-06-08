import MultiplayerSocketContext from "../context/MultiplayerSocketProvider";
import { useContext } from "react";

const useMultiplayerSocket = () => {
    return useContext(MultiplayerSocketContext);
}

export default useMultiplayerSocket;