import {Overview} from "./component/overview";
import React from "react";
import {IndexRoute, Route} from "react-router";

export default (
  <Route path="/">
    <IndexRoute component={Overview}/>
  </Route>
);