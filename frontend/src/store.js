import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'

import { screenerReducer } from './reducers/screenerReducer'

const reducer = combineReducers({
    screener: screenerReducer
})

const screenerTickersFromStorage =
    localStorage.getItem('tickers')
        ? JSON.parse(localStorage.getItem('tickers'))
        : {}

const initialState = {
    screener: { tickers: screenerTickersFromStorage }
}

const middleware = [thunk]

const store = createStore(reducer, initialState, composeWithDevTools(applyMiddleware(...middleware)))

export default store;

