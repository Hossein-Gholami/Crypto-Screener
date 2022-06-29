import axios from 'axios'
import { 
  ADD_TICKER_REQUEST,
  ADD_TICKER_SUCCESS,
  ADD_TICKER_FAIL,
  TICKERS_UPDATING,
  TICKERS_UPDATED } from '../constants/ScreenerConstants'


export const addTicker = (ticker) => async (dispatch, getState) => {
  try {
  
    dispatch({ type:ADD_TICKER_REQUEST })

    const { data } = await axios.post('/screener/add/', ticker)

    dispatch({
      type: ADD_TICKER_SUCCESS,
      payload: {
        name: data.name,
        price: Number(data.price),
      }
    })

    localStorage.setItem('tickers', JSON.stringify(getState().screener.tickers))
  
  } catch (error) {
    
    dispatch({
      type: ADD_TICKER_FAIL,
      error: error.response && error.response.data.message
        ? error.response.data.message
        : error.message
    })

  }
}


export const updateTickers = ({ tickers }) => (dispatch, getState) => {
  dispatch({ type: TICKERS_UPDATING })

  const _tickers = getState().screener.tickers
  
  Object.keys(_tickers).map((key,index)=>{
    _tickers[key] = tickers[key]
  })

  dispatch({
    type: TICKERS_UPDATED,
    payload: _tickers
  })

  localStorage.setItem('tickers', JSON.stringify(getState().screener.tickers))

}

