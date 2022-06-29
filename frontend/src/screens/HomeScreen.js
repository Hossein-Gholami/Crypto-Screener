import { useEffect } from 'react'
import { Container, ListGroup } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import { w3cwebsocket as W3CWebSocket } from 'websocket'

import { updateTickers } from '../actions/ScreenerActions'

function HomeScreen() {
  const { tickers } = useSelector(state => state.screener)
  const dispatch = useDispatch()

  useEffect(() => {

    const socketClient = new W3CWebSocket('ws://127.0.0.1:8000/ws/screener/')

    socketClient.onopen = () => {
      console.log('WebSocket client connected');
    }

    socketClient.onclose = () => {
      console.log('WebSocket Closed!');
    }

    socketClient.onmessage = (message) => {
      // console.log(message)
      const data = JSON.parse(message.data)
      // console.log(tickers)
      // console.log(data.tickers)
      dispatch(updateTickers(data))
    }

  }, [dispatch])

  return (
    <Container md={6} my={3}>
      <ListGroup as="ul" variant="flush">
      {Object.keys(tickers).map((key,index) => {
        return (
          <ListGroup.Item key={index} as="li" className="d-flex justify-content-between align-items-start">
            <div className="ms-2 me-auto">
              <div className="fw-bold">{key}</div>
              {tickers[key]}
            </div>
            {/*<Badge bg="primary" pill>
              14
            </Badge>*/}
          </ListGroup.Item>
        );
      })}
      </ListGroup>
    </Container>
  )
}

export default HomeScreen;

