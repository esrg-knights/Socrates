import {succesfullLogin} from "../actions/AuthActions";
import ApiService from "./ApiService";
import authStore from '../stores/AuthStore';

export class AuthService {
  login(username, password) {
    new ApiService().post('http://localhost:8000/api/auth/', {username: username, password: password}).then(
      response => response /*authStore.dispatch(succesfullLogin(username, response.token)) */
    );
  }
}