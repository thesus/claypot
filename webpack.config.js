const path = require('path');
const fs = require('fs');

const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry () {
        // Add entry for every file in claypot/contrib/static/js
        let folder = path.resolve(__dirname, 'claypot/contrib/static/js')
        let files = fs.readdirSync(folder)

        entries = {}
        files.forEach((file) => {
            name = file.split('.').slice(0, -1).join('.')
            entries[name] = path.resolve(folder, file)
        })
        entries['style'] = path.resolve(__dirname, 'claypot/contrib/static/scss/style.scss')
        return entries
    },
    mode: 'none',
    output: {
        path: path.resolve(__dirname, 'claypot/contrib/static/vendor'),
        filename: '[name].js'
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        },
        extensions: ['.js']
    },
    optimization: {
        splitChunks: {
            cacheGroups: {
                vendors: {
                    test: /\.js$/,
                    name: 'vendor',
                    chunks: 'initial',
                    minChunks: 1
                }
            }
        }
    },
	module: {
        rules: [
            {
                enforce: "pre",
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: "eslint-loader"
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        "presets": [
                            "env"
                        ]
                    }
                }
            },
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                    },
                    {
                        loader: "css-loader",
                    },
                    {
                        loader: "sass-loader",
                    }
                ]
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].css',
        })
    ]
}
