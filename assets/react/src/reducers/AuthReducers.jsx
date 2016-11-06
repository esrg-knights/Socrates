import {LOGIN_SUCCESFULL} from "../actions/AuthActions";
import combineReducers from 'redux/src/combineReducers';

function loginReducer(state = [], action) {
  switch (action.type) {
    case LOGIN_SUCCESFULL:
      return [
        ...state,
        {
          logged_in: true,
          username: action.username,
          jwt: action.jwt
        }
      ];
    default:
      return state;
  }
}

function noneReducer(state = [], action){
  return state;
}

let authReducer = combineReducers({
  loginReducer
});

export default authReducer;