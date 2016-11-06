import React from "react";
import {Route, Router, IndexRoute} from "react-router";
import Overview from "./component/overview";
import Profile from "./component/profile";
import DinnerList from "./component/dinnerList";

export default (
  <Router history={history}>
    <Route path="/" component={Overview}>
      <IndexRoute component={Profile} />
      <Route path="dinner" component={DinnerList} />
    </Route>
  </Router>
);