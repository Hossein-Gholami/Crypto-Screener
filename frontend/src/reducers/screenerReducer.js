import {
    ADD_SYMBOL_REQUEST,
    ADD_SYMBOL_SUCCESS,
    ADD_SYMBOL_FAIL,
    TICKERS_UPDATING,
    TICKERS_UPDATED
} from "../constants/symbolConstants";

export const screenerReducer = (state = { tickers: [] }, action) => {
    switch (action.type) {
        case ADD_SYMBOL_REQUEST:
            return {
                ...state,
                subscribing: true,
            }
        case ADD_SYMBOL_SUCCESS:
            const { name, price } = action.payload

            // const tickerExist = name in Object.keys(state.tickers)

            const tickers = state.tickers
            tickers[name] = price
            return {
                tickers: tickers,
            }

        // if (tickerExist) {
        //     const tickers = state.tickers
        //     tickers[name] = price
        //     return {
        //         ...state,
        //         tickers: tickers,
        //     }
        // }
        // else {
        //     const tickers = state.tickers
        //     tickers[name] = price
        //     return {
        //         ...state,
        //         tickers: tickers,
        //     }
        // }
        // return {
        //     tickers: Object.keys(state.tickers).map((k, i) => { k === name ? state.tickers[name] = price : state.tickers[name] })
        // }
        // const tickerExists = state.tickers.find(x => console.log('key', x.key) && x.key === name)
        // const ticker = {}
        // ticker[name] = price
        // console.log(ticker)

        // if (tickerExists) {
        //     // console.log('ticker doesn\'t exist')
        //     // console.log(state.tickers.map(x => x.key === tickerExists.key ? ticker : x))
        //     return {
        //         ...state,
        //         tickers: state.tickers.map(x => x.key === tickerExists.key ? ticker : x),
        //     }
        // } else {
        //     // console.log('ticker doesn\'t exist')
        //     // console.log([...state.tickers, ticker])
        //     return {
        //         ...state,
        //         tickers: [...state.tickers, ticker]
        //     }
        // }
        case ADD_SYMBOL_FAIL:
            return {
                tickers: state.tickers,
                error: action.payload,
            }
        case TICKERS_UPDATING:
            return {
                ...state,
                updating: true,
            }
        case TICKERS_UPDATED:
            return {
                // ...state,
                tickers: action.payload,
            }
        default:
            return state
    }
}

