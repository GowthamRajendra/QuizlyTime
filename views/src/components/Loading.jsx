// Loading icon, shown when fetching data from the server

import React from 'react'
import Spinner from 'react-bootstrap/Spinner'

function Loading() {
    return <div className="position-absolute top-50 start-50 translate-middle">
        <Spinner animation='grow'></Spinner>
    </div>
}

export default Loading