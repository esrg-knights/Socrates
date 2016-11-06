import {Drawer, AppBar, MenuItem, FlatButton} from "material-ui";
import React, {Component} from "react";

export default class Overview extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      menuOpen: false
    };

    this.handleTouchTap = this.handleTouchTap.bind(this);
  }


  handleTouchTap(e) {
    this.setState({
      menuOpen: true
    });
    console.log("Clicked");
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
            docked={true}>
            <h2>Eetlijst</h2>
            <MenuItem >Eetlijst </MenuItem>
            <MenuItem >Profiel</MenuItem>
          </Drawer>
        </AppBar>
        {this.props.children}
      </div>
    )
  }
}