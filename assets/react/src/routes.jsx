import React from "react";
import {Route, Router, IndexRoute} from "react-router";
import Overview from "./component/overview";
import ProfileComponent from "./component/profile";

export default (
  <Router history={history}>
    <Route path="/" component={Overview}>
      <IndexRoute component={ProfileComponent} />
    </Route>
  </Router>
);