module.exports = {
    devServer: {
      proxy: 'https://inf551-b0e88.firebaseio.com/daily_situation',
    },
    css: {
      loaderOptions: {
        less: {
          modifyVars: {
            'primary-color': '#1DA57A',
            'link-color': '#1DA57A',
            'border-radius-base': '2px',
          },
          javascriptEnabled: true,
        },
      },
    },
  };