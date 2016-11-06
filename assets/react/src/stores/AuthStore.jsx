import authReducer from '../reducers/AuthReducers';
import {createStore} from 'redux';

let authStore = createStore(authReducer);

export default authStore;