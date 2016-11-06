import BaseStore from "./BaseStore";
import {LOGIN_SUCCESFULL} from "../actions/AuthActions";

class AuthStore extends BaseStore {
  _user;
  _jwt;


  get user() {
    return this._user;
  }

  get jwt() {
    return this._jwt;
  }

  constructor() {
    super();
    this._user = null;
    this._jwt = null;
  }

  registerToActions(action) {
    switch (action.type) {
      case LOGIN_SUCCESFULL:
        this._user = action.username;
        this._jwt = action.jwt;
        break;
      default:
        break;
    }
    this.emitChange();
  }

  isLoggedIn() {
    return !!this.user;
  }
}

export default new AuthStore();