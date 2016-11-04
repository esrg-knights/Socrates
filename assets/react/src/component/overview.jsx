import AppBar from 'material-ui/AppBar';
import React from 'react';

export default class Overview extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <AppBar
          title="Overview"
        />
        <h1>Hello</h1>
      </div>
    )
  }
}