const path = require('path');

const HtmlWebpackPlugin = require('html-webpack-plugin');

const pkg = require('./package.json');


module.exports = {
  entry: path.resolve(__dirname, './src/main.jsx'),
  output: {
    path: path.resolve(__dirname, 'build/'),
    filename: 'bundle.js'
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  },
  devServer: {
    contentBase: path.resolve(__dirname, 'src')
  },
  devtool: 'inline-source-map',
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        loader: 'babel'
      },
      {
        test: /\.json$/,
        loader: 'json'
      },
      {
        test: /\.css$/,
        loaders: ['style', 'css']
      },
      {
        test: /\.(eot|gif|jpe?g|png|svg|ttf|woff2?)(\?.*)?$/,
        loaders: ['file']
      }
    ]
  },
  externals: {
    // Workaround for https://github.com/airbnb/enzyme/issues/47
    'react/addons': true,
    'react/lib/ExecutionEnvironment': true,
    'react/lib/ReactContext': true
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: pkg.name
    })
  ]
};