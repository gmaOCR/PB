const { resolve } = require('path');

module.exports = {
  entry: './static/js/that_open.js',
  output: {
    filename: 'that_open_bundle.js',
    path: resolve(__dirname, 'static/dist'),
    publicPath: '/static/dist/',
    library: {
      type: 'umd',
      name: 'ThatOpen',
      export: 'panel',
    },
  },
  resolve: {
    fallback: {
      "path": require.resolve("path-browserify")
    },
    modules: ['node_modules'],
    alias: {
      '@thatopen/ui': resolve(__dirname, 'node_modules/@thatopen/ui'),
    },
  },
  mode: 'development',
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
    ],
  },
};
