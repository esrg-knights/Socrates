import {Drawer, AppBar, MenuItem, FlatButton} from "material-ui";
import React, {Component} from "react";
import {Link} from "react-router";

export default class Overview extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      menuOpen: false
    };

    this.handleTouchTap = this.handleTouchTap.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.handleRequestChange = this.handleRequestChange.bind(this);
  }


  handleTouchTap(e) {
    this.setState({
      menuOpen: true
    });
  }

  handleClose() {
    this.setState({
      menuOpen: false
    });
  }

  handleRequestChange(open) {
    this.setState({
      menuOpen: open
    })
  }

  render() {
    return (
      <div>
        <AppBar
          title="Knights of the Kitchen Table"
          onLeftIconButtonTouchTap={this.handleTouchTap}
          iconClassNameright="muidocs-icon-navigation-expand-more"
          iconElementRight={<FlatButton label="Save"/>}>
          <Drawer
            open={this.state.menuOpen}
            docked={false}
            onRequestChange={this.handleRequestChange}>
            <h2>Eetlijst</h2>
            <MenuItem containerElement={<Link to="/"/>} onTouchTap={this.handleClose}>Profile </MenuItem>
            <MenuItem containerElement={<Link to="/dinner"/>} onTouchTap={this.handleClose}>Dinner</MenuItem>
          </Drawer>
        </AppBar>
        {this.props.children}
      </div>
    )
  }
}