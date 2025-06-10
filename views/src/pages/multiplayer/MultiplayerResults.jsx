import { useLocation } from "react-router-dom"

function MultiplayerResults() {
    const location = useLocation()
    const results = location.state?.results ?? []

    return <div>
        <ol>
            {results.map(({name, score}) => (
                <li>{name}: {score}</li>
            ))}
        </ol>
    </div>
}

export default MultiplayerResults