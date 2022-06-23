import { useState } from 'react'
import { useDispatch } from 'react-redux'
import { Col, Container, Form, Row, Button } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import { addSymbol } from '../actions/symbolActions'

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
        e.preventDefault();
        const symbol = { name }
        // console.log(symbol)
        setName('')
        dispatch(addSymbol(symbol))
        navigate("/", { replace: true })
    }

    return (
        <Container>
            <Form method="post" onSubmit={handleSubmit}>
                <Form.Group as={Row} className="mb-3" controlId="formHorizontalEmail">
                    <Form.Label column sm={2}>
                        Symbol
                    </Form.Label>
                    <Col sm={10}>
                        <Form.Control type="text" placeholder="Symbol Name" value={name} onChange={(e) => setName(e.target.value)} required />
                    </Col>
                </Form.Group>
                <Form.Group as={Row} className="mb-3">
                    <Col sm={{ span: 10, offset: 2 }}>
                        <Button type="submit">Add</Button>
                    </Col>
                </Form.Group>
            </Form>
        </Container>
    )
}

export default AddSymbol;
