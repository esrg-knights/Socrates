import {LOGIN_SUCCESFULL} from "../actions/AuthActions";
import combineReducers from 'redux/src/combineReducers';
import {LOGOUT} from "../actions/AuthActions";

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
    case LOGOUT:
      return [
        ...state,
        {
          logged_in: false
        }
      ];
    default:
      return [
        ...state,
        {
          logged_in: false
        }
      ];
  }
}

function noneReducer(state = [], action){
  return state;
}

let authReducer = combineReducers({
  loginReducer
});

export default authReducer;