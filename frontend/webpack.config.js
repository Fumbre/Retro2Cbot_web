const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

module.exports = (env, argv) => {
  const isDev = argv.mode === "development";

  return {
    entry: "./assets/scripts/main.js",
    mode: isDev ? "development" : "production",

    output: {
      path: path.resolve(__dirname, "dist"),
      filename: isDev ? "bundle.js" : "bundle.[contenthash].js",
      publicPath: '/',
      clean: true,
    },

    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use:
          {
            loader: 'babel-loader',
          },
        },
        {
          test: /\.(scss|sass)$/,
          use: [
            isDev ? "style-loader" : MiniCssExtractPlugin.loader,
            "css-loader",
            "sass-loader"
          ],
        },
      ],
    },

    plugins: [
      new WebpackManifestPlugin(),
      !isDev &&
      new MiniCssExtractPlugin({
        filename: "style.[contenthash].css",
      }),
    ].filter(Boolean),
    devtool: isDev ? "source-map" : false,
    watch: isDev,
  }
};
