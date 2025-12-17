import path from 'node:path';
import MiniCssExtractPlugin from "mini-css-extract-plugin";
import { WebpackManifestPlugin } from 'webpack-manifest-plugin';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const config = (env, argv) => {
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
            {
              loader: 'sass-loader',
              options: {
                sassOptions: {
                  indentedSyntax: true,
                  loadPaths: ["assets/style"],
                },
              },
            },
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

export default config;
