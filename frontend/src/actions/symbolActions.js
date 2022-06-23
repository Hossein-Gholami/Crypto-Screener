import axios from 'axios'
import {
    ADD_SYMBOL_REQUEST,
    ADD_SYMBOL_SUCCESS,
    ADD_SYMBOL_FAIL,
    TICKERS_UPDATING,
    TICKERS_UPDATED
} from "../constants/symbolConstants";


export const addSymbol = (symbol) => async (dispatch, getState) => {
    try {

        dispatch({ type: ADD_SYMBOL_REQUEST })

        const { data } = await axios.post('/screener/add/', symbol)

        dispatch({
            type: ADD_SYMBOL_SUCCESS,
            payload: {
                name: data.symbol_name,
                price: Number(data.last_price),
            }
        })

        localStorage.setItem('tickers', JSON.stringify(getState().screener.tickers))

    } catch (error) {
        dispatch({
            type: ADD_SYMBOL_FAIL,
            payload: error.response && error.response.data.message
                ? error.response.data.message
                : error.message
        })
    }
}

export const updateTickers = ({ tickers }) => (dispatch, getState) => {
    dispatch({ type: TICKERS_UPDATING })
    tickers = JSON.parse(tickers)

    const _tickers = getState().screener.tickers
    Object.keys(_tickers).map((key, index) => {
        // console.log(index, key, tickers[key])
        _tickers[key] = tickers[key]
    })

    dispatch({
        type: TICKERS_UPDATED,
        payload: _tickers,
    })
    // console.log('tickers:', JSON.stringify(getState().screener.tickers))
    localStorage.setItem('tickers', JSON.stringify(getState().screener.tickers))
}
