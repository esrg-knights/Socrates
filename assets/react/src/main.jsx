import './main.css';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import React from 'react';
import {Router} from 'react-router';
import {hashHistory} from 'react-router';
import injectTapEventPlugin from 'react-tap-event-plugin';
import generateTheme from './theming/generate-theme'
import {render} from 'react-dom';
import routes from './routes';


const wrapper = document.createElement('div');
wrapper.id = 'react-wrapper';
wrapper.className = 'container';
document.body.appendChild(wrapper);


injectTapEventPlugin();


const app = {
  primaryColor: 'green',
  secondaryColor: 'blue',
  dark: false
};


render(
  <MuiThemeProvider muiTheme={generateTheme(app)}>
    <Router
      history={hashHistory}
      routes={routes}
    />
  </MuiThemeProvider>,
  wrapper
);
