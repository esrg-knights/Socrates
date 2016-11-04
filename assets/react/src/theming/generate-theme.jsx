import * as colors from 'material-ui/styles/colors';
import {darkBlack} from 'material-ui/styles/colors';
import {fade} from 'material-ui/utils/colorManipulator';
import {fullBlack} from 'material-ui/styles/colors';
import {fullWhite} from 'material-ui/styles/colors';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import {grey100} from 'material-ui/styles/colors';
import {grey300} from 'material-ui/styles/colors';
import {grey400} from 'material-ui/styles/colors';
import {grey500} from 'material-ui/styles/colors';
import {grey600} from 'material-ui/styles/colors';
import spacing from 'material-ui/styles/spacing';
import {white} from 'material-ui/styles/colors';


/**
 * Generate a material-ui theme from Appsemble app configuration.
 *
 * The generated themes are based on [lightBaseTheme][lightBaseTheme] and [darkBaseTheme][darkBaseTheme] respectively.
 *
 * @see http://www.material-ui.com/#/customization/themes for details.
 *
 * [darkBaseTheme]: https://github.com/callemall/material-ui/blob/master/src/styles/baseThemes/darkBaseTheme.js
 * [lightBaseTheme]: https://github.com/callemall/material-ui/blob/master/src/styles/baseThemes/lightBaseTheme.js
 *
 * @param {Object} app The Appsemble app defining the theme.
 * @returns {Object} A preset theme that can be passed to `MuiThemeProvider.muiTheme`.
 */
export default function generateTheme(app) {
  const {primaryColor, secondaryColor, dark} = app;

  let palette;

  if (dark) {
    palette = {
      primary1Color: colors[`${primaryColor}700`],
      primary2Color: colors[`${primaryColor}700`],
      primary3Color: grey600,
      accent1Color: colors[`${secondaryColor}A200`],
      accent2Color: colors[`${secondaryColor}A200`],
      accent3Color: colors[`${secondaryColor}A100`],
      textColor: fullWhite,
      secondaryTextColor: fade(fullWhite, 0.7),
      alternateTextColor: '#303030',
      canvasColor: '#303030',
      borderColor: fade(fullWhite, 0.3),
      disabledColor: fade(fullWhite, 0.3),
      pickerHeaderColor: fade(fullWhite, 0.12),
      clockCircleColor: fade(fullWhite, 0.12)
    };
  } else {
    palette = {
      primary1Color: colors[`${primaryColor}500`],
      primary2Color: colors[`${primaryColor}700`],
      primary3Color: grey400,
      accent1Color: colors[`${secondaryColor}A200`],
      accent2Color: grey100,
      accent3Color: grey500,
      textColor: darkBlack,
      secondaryTextColor: fade(darkBlack, 0.54),
      alternateTextColor: white,
      canvasColor: white,
      borderColor: grey300,
      disabledColor: fade(darkBlack, 0.3),
      pickerHeaderColor: colors[`${primaryColor}500`],
      clockCircleColor: fade(darkBlack, 0.07),
      shadowColor: fullBlack
    };
  }

  return getMuiTheme({
    fontFamily: 'Roboto',
    palette,
    spacing
  });
}
