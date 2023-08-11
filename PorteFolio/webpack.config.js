const path = require('path');
const webpack = require('webpack');
const threeMeshBVHPackage = require('three-mesh-bvh/package.json');
const three = require('three/package.json');

module.exports = {
  resolve: {
      extensions: ['.js', '.json', '.mjs'],
      modules: ['node_modules'],
      alias: {
          'path.js': 'path',


          'web-ifc-viewer': 'web-ifc-viewer/dist/index.js',
          './edgeUtils': path.resolve(__dirname, 'node_modules/web-ifc-viewer/dist/components/import-export/edges-vectorizer/edgeUtils.js'),
          '../../base-types': path.resolve(__dirname, 'node_modules/web-ifc-viewer/dist/base-types.js'),
          '../../utils/ThreeUtils': path.resolve(__dirname, 'node_modules/web-ifc-viewer/dist/utils/ThreeUtils.js'),
          './components': path.resolve(__dirname, 'node_modules/web-ifc-viewer/dist/components/index.js'),
          './components/display/clipping-planes/clipping-edges': path.resolve(__dirname, 'node_modules/web-ifc-viewer/dist/components/display/clipping-planes/clipping-edges.js'),
          './base-types': path.resolve(__dirname, 'node_modules/web-ifc-viewer/dist/base-types.js'),

          'web-ifc.js': 'web-ifc/web-ifc-api-node.js',

          'three.js': path.resolve('node_modules/three', three.main),
          'three/examples/jsm/utils/BufferGeometryUtils': 'three/examples/jsm/utils/BufferGeometryUtils.js',
          'three-mesh-bvh.js': path.resolve('node_modules/three-mesh-bvh', threeMeshBVHPackage.main),

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
    filename: 'bundle.js',
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
new webpack.NormalModuleReplacementPlugin(/^(.*)(?<!\.js)$/, function(resource) {
    if ((resource.context.includes('web-ifc-viewer') || resource.context.includes('node_modules')) && !resource.request.endsWith('.js')) {
        resource.request += '.js';
    }
}),

],


};
