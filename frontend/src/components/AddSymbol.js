import { useState } from 'react'
import { Container, Form, Button, Col, Row } from 'react-bootstrap'
import { useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'

import { addTicker } from '../actions/ScreenerActions'

function AddSymbol() {

    // const JustMounted = useRef(true)
    const [name, setName] = useState('')
    const dispatch = useDispatch()
    const navigate = useNavigate()

    // useEffect(() => {
    //     if (JustMounted.current) {
    //         JustMounted.current = false;
    //         dipatch(init())
    //     }
    // }, [dispatch, setSymbol])

    const handleSubmit = (e) => {
        e.preventDefault()
        const ticker = {name}
        setName('')
        dispatch(addTicker(ticker))
        navigate("/", { replace: true })
    }

    return (
        <Container className="py-3">
            <Form method="post" onSubmit={handleSubmit}>
                <Form.Group as={Row} className="mb-3">
                    <Form.Label column sm={2}>Ticker: </Form.Label>
                    <Col sm={10}>
                        <Form.Control type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Ticker Name" required/>
                    </Col>
                </Form.Group>
                <Form.Group as={Row} className="mb-3">
                    <Col sm={{ span:10, offset:2 }}>
                        <Button type="submit">Subscribe</Button>
                    </Col>
                </Form.Group>
            </Form>
        </Container>
    )
}

export default AddSymbol;
