# boarboardash-crawler

## 目录结构

- /sites/：一个包，里面提供了爬取不同网站的具体逻辑
- /init_database.py：初始化数据库，只需要运行一次
- /models.py：定义了数据库的对象类型
- /api_models.py：定义了发送请求的数据类型
- /config_example.py：配置文件的例子，不会加载
- /config.py：实际加载的配置文件
- /conda_env.yaml：conda环境的依赖清单
- /main.py：主程序，每小时定时爬取网页