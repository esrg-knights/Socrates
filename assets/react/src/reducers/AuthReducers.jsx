import {LOGIN_SUCCESFULL} from "../actions/AuthActions";

function loginReducer(state = [], action) {
  switch (action.type) {
    case LOGIN_SUCCESFULL:
      return [
        ...state,
        {
          logged_in: true,
          username: action.username,
          jwt: action.token
        }
      ];
    default:
      return state;
  }
}

export default loginReducer;