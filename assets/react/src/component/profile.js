import * as React from "react";
import {TextField} from "material-ui";
import {AuthService} from "../service/AuthService";
import authStore from "../stores/AuthStore";
import {hashHistory} from "react-router";
import {successfullLogin} from "../actions/AuthActions";

export default class Profile extends React.Component {
  constructor(props) {
    super(props);
  }



  render() {
    return (
      <div>
        <h1>Hello</h1>
      </div>
    )
  }
}