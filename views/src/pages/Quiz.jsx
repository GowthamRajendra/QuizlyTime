// TODO
// quiz settings page
// quiz game page

import { useEffect } from "react"
import useAxios from "../hooks/useAxios"

function Quiz() {
    const axios = useAxios()

    useEffect(() => {
        async function testProtected() {
            try {
                const response = await axios.get(
                    '/protected'
                )
    
                console.log(JSON.stringify(response?.data))
    
            } catch (err) {
                if (!err?.response) {
                    console.error("No response")
                }
                else if (err.response) {
                    console.error(err.response.data.message)
                }
                else {
                    console.error(err)
                }
            }
        }

        testProtected()

        return () => {
            console.log('cleanup')
        }
    }, [])

    return (
        <div>
            Quiz Page
        </div>
    )
}

export default Quiz