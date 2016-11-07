import * as React from "react";
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
    this.userChange = this.userChange.bind(this);
    this.passwordChange = this.passwordChange.bind(this);
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

  userChange(val) {
    this.setState({
      user: val.target.value
    })
  }

  passwordChange(val){
    this.setState({
      password: val.target.value
    })
  }

  render() {
    return (
      <div>
        <form role="form">
          <div>
            <TextField
              hintText="Username"
              value={this.state.user}
              onChange={this.userChange}
            /><br />
            <TextField
              hintText="Password Field"
              floatingLabelText="Password"
              type="password"
              value={this.state.password}
              onChange={this.passwordChange}
            /><br />
          </div>
          <button type="submit" onClick={this.login}>Submit</button>
        </form>
      </div>
    )
  }
}