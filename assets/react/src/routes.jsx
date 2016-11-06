import React from "react";
import {Route, Router, IndexRoute} from "react-router";
import Overview from "./component/overview";
import Profile from "./component/profile";
import DinnerList from "./component/dinnerList";
import Login from "./component/login";

export default (
  <Router history={history}>
    <Route path="/" component={Overview}>
      <IndexRoute component={Login} />
      <Route path="profile" component={Profile} />
      <Route path="dinner" component={DinnerList} />
    </Route>
  </Router>
);