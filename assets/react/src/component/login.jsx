import * as React from "react";
import {Binder} from "react-binding";
import {TextField} from "material-ui";
import {AuthService} from "../service/AuthService";
import authStore from "../stores/AuthStore";
import {hashHistory} from "react-router";
import {successfullLogin} from "../actions/AuthActions";

export default class Login extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      user: '',
      password: ''
    };

    this.subscription = authStore.subscribe(() => {
      console.log(authStore.getState());
      if (localStorage.getItem("jwt") != "") {
        hashHistory.push('profile');
      }
    });

    this.login = this.login.bind(this);
  }

  componentDidMount() {
    if (localStorage.getItem("jwt") != "" && localStorage.getItem("username") != "") {
      authStore.dispatch(successfullLogin(localStorage.getItem("username"), localStorage.getItem("jwt")));
    }
  }

  login(e) {
    e.preventDefault();

    console.log(this.state);

    new AuthService().login(this.state.user, this.state.password);
  }

  render() {
    return (
      <div>
        <form role="form">
          <div>
            <TextField
              hintText="Username"
            /><br />
            <TextField
              hintText="Password Field"
              floatingLabelText="Password"
              type="password"
            /><br />
          </div>
          <button type="submit" onClick={this.login}>Submit</button>
        </form>
      </div>
    )
  }
}