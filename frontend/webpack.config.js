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
      chunkFilename: 'chunks/[name].[contenthash].js'
    },

    resolve: {
      alias: {
        '@pages': path.resolve(__dirname, 'assets/scripts/pages/'),
        '@partials': path.resolve(__dirname, 'assets/scripts/partials/'),
        '@websocket': path.resolve(__dirname, 'assets/scripts/websocket/'),
      },
      extensions: ['.js']
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
        {
          test: /\.(png|jpg|jpeg|gif|svg)$/i,
          type: 'asset/resource',
          generator: {
            filename: 'images/[name].[hash][ext]',
          },
        }
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

path.resolve()

export default config;
