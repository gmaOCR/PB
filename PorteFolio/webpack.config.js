//const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

const path = require('path');
const webpack = require('webpack');
const threeMeshBVHPackage = require('three-mesh-bvh/package.json');
const three = require('three/package.json');
//const web_ifc_three = require('web-ifc-three/package.json');

module.exports = {
    devtool: 'eval-source-map',
  resolve: {
        fallback: {
          fs: false,
          path: false,
          perf_hooks: false,
          worker_threads: false,
        },
      extensions: ['.js', '.json', '.mjs'],
      modules: ['node_modules'],
      alias: {
          'web-ifc-viewer': 'web-ifc-viewer/dist/index.js',
          'web-ifc.js': 'web-ifc/web-ifc-api-node.js',
          'three': path.resolve(__dirname, 'node_modules/three'),
          'three.js': path.resolve(__dirname, 'node_modules/three/build/three.module.js'),
          'three-mesh-bvh.js': path.resolve('node_modules/three-mesh-bvh', threeMeshBVHPackage.main),
          'gsap.js': path.resolve(__dirname, 'node_modules/gsap/dist/gsap.js'),
          'camera-controls.js': path.resolve(__dirname, 'node_modules/camera-controls/dist/camera-controls.js'),
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
            presets: ['@babel/preset-env'],
            sourceMaps: true
          }
        }
      }
    ]
  },
plugins: [
        new webpack.ProvidePlugin({
            THREE: 'three'
        }),
//        new BundleAnalyzerPlugin(),
        new webpack.NormalModuleReplacementPlugin(/^\.\/components$/, function(resource) {
            resource.request = './components/index.js';
        }),

        new webpack.NormalModuleReplacementPlugin(/^(.*)(?<!\.js)$/, function(resource) {
            // Nativ Node.js module to exclude
            if (['fs', 'perf_hooks', 'worker_threads', 'crypto', 'path'].includes(resource.request)) {
                return;
            }

            // If request './components/' and not end with '.js', add '.js'
            if (resource.request.startsWith('./components/') && !resource.request.endsWith('.js')) {
                resource.request += '.js';
            }

            // If path contain "web-ifc-viewer" or "node_modules" (but not "web-ifc-three") and not end with ".js"
            if ((resource.context.includes('web-ifc-viewer') || (resource.context.includes('node_modules') && !resource.request.startsWith('web-ifc-three'))) && !resource.request.endsWith('.js')) {
                resource.request += '.js';
            }
        }),
    ],
};
