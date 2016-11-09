import {successfullLogin} from "../actions/AuthActions";
import ApiService from "./ApiService";
import authStore from '../stores/AuthStore';
import {logout} from "../actions/AuthActions";

export class AuthService {
  login(username, password) {
    new ApiService().post('auth/token/', {username: username, password: password}).then(
      response => authStore.dispatch(successfullLogin(username, response))
    );
  }

  logout(){
    authStore.dispatch(logout())
  }
}