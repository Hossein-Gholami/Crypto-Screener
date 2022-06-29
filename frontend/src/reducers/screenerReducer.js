import { 
    ADD_TICKER_REQUEST,
    ADD_TICKER_SUCCESS,
    ADD_TICKER_FAIL,
    TICKERS_UPDATING,
    TICKERS_UPDATED } from '../constants/ScreenerConstants'
  
  
  export const screenerReducer = (state = { tickers:{} }, action) => {
    switch(action.type) {
      // SUBSCRIBING TO ANOTHER TICKER CASES
      case ADD_TICKER_REQUEST:
        return {
          ...state,
          subscribing:true,
        }
      case ADD_TICKER_SUCCESS:
        const { name, price } = action.payload
        const tickers = state.tickers
        tickers[name] = price
        return {
          tickers: tickers,
        }
      case ADD_TICKER_FAIL:
        return {
          tickers: state.tickers,
          error: action.payload,
        }
      // UPDATING TICKERS CASES
      case TICKERS_UPDATING:
        return {
          ...state,
          updating: true,
        }
      case TICKERS_UPDATED:
        return {
          tickers: action.payload
        }
      default:
        return state
    }
  }
  