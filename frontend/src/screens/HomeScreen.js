import { useRef, useEffect } from 'react'
import { Container, ListGroup } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import { w3cwebsocket as W3CWebSocket } from 'websocket'
import { updateTickers } from '../actions/symbolActions'

function HomeScreen() {

  const JustMounted = useRef(true)
  const dispatch = useDispatch()
  const { tickers } = useSelector(state => state.screener)

  useEffect(() => {
    if (JustMounted.current) {
      JustMounted.current = false
      console.error('JUST MOUNTED')
    }
    const socketClient = new W3CWebSocket('ws://127.0.0.1:8000/ws/screener/')

    socketClient.onopen = () => {
      console.log('WebSocket Client Connected');
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

  }, [dispatch, JustMounted])

  return (
    <Container>
      <div>
        {Object.keys(tickers).map((key, index) => {
          return (
            <ListGroup.Item key={index} as="li" className="d-flex justify-content-between align-items-start">
              <div className="ms-2 me-auto">
                <div className="fw-bold">{key}</div>
                {tickers[key]}
              </div>
              {/* <Badge bg="primary" pill>
              14
            </Badge> */}
            </ListGroup.Item>
          );
        })}

      </div>
      <ListGroup as="ul" variant="flush">

      </ListGroup>
    </Container>
  )
}

export default HomeScreen;

