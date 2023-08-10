const path = require('path');
const webpack = require('webpack');

module.exports = {
  resolve: {
      extensions: ['.js', '.json', '.mjs'],
      modules: ['node_modules'],
      alias: {
          'web-ifc-viewer': 'web-ifc-viewer/dist/index.js',
      },
      mainFields: ['browser', 'module', 'main'],
      fullySpecified: false
  },
  experiments: {
    asyncWebAssembly: true
  },
  mode: 'development',
  entry: './static/js/preview.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'static/dist'),
  },
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      }
    ]
  },
  plugins: [
    new webpack.NormalModuleReplacementPlugin(/^(.*)([^\.js])$/, function(resource) {
      if (resource.context.includes('node_modules/web-ifc-viewer') && !resource.request.endsWith('.js')) {
        resource.request += '.js';
      }
    }),
  ],

};
