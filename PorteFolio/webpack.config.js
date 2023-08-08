const path = require('path');
//const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
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
        test: /\.wasm$/,
            type: 'webassembly/async'
        },
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
  }
};
