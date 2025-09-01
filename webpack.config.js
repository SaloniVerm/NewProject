const path = require('path');
const webpack = require('webpack'); // Add this line


module.exports = {
    entry: '/static/js/web3modal.js',  // Replace with your entry file path
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'static/newdist6'),  // Replace with your output directory
    },
    resolve: {
        fallback: {
            "stream": require.resolve("stream-browserify"),
            "http": require.resolve("stream-http"),
            "https": require.resolve("https-browserify"),
            "os": require.resolve("os-browserify/browser"),
            "buffer": require.resolve("buffer")
        }
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
        new webpack.ProvidePlugin({
            Buffer: ['buffer', 'Buffer'],
        }),
    ],
};
