import React from "react";
import {Route, Router, IndexRoute} from "react-router";
import Overview from "./component/overview";
import DinnerList from "./component/dinner";
import Login from "./component/login";
import Profile from "./component/profile";

export default (
  <Router history={history}>
    <Route path="/" component={Overview}>
      <IndexRoute component={Login} />
      <Route path="profile" component={Profile} />
      <Route path="dinner" component={DinnerList} />
    </Route>
  </Router>
);