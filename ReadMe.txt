
【 本 地 配 置 项 目 开 发 环 境 】

1.配置本地虚拟环境
（1）修改：requirements.txt
（2）执行：sh -x venv_install.sh

2.配置gulpfile依赖
（1）修改：gulpfile_install.sh
（2）执行：sh -x gulpfile_install.sh


########################################################################################################################


【 本地 Mac 相关 】

1.uWSGI配置文件：./vassals/mac_app_uwsgi.ini
（1）启动 uWSGI 命令 在 ./start_uwsgi_local.sh 脚本
（2）停止 uWSGI 命令 在 ./stop_uwsgi.sh 脚本

2.上传 GitHub 需要被忽略的文件
（1）Logs、Reports -> 临时生产的 日志、报告
（2）vassals_local、venv -> 本地的 uWSGI配置、python3虚拟环境
（3）node_modules、gulpfile.js、package.json、package-lock.json -> 供本地启动使用的gulp工具

3.访问地址（ server.py 启动 ）：
（1）接口地址 -> http://127.0.0.1:6002/
               http://127.0.0.1:6002/API/index
               http://127.0.0.1:6002/API/get_project_case_list/<pro_name>

4.访问地址（ uwsgi 启动 ）：
（1）用例页面 -> http://localhost:6010/api_local/APP/index
（2）测试报告 -> http://127.0.0.1:6010/test_report_local/<pro_name>/[APP_report]<pro_name>.html
（3）接口地址 -> http://127.0.0.1:6010/api_local/
               http://127.0.0.1:6010/api_local/WEB/sync_run_case
               http://127.0.0.1:6010/api_local/WEB/get_img/5e5cac9188121299450740b3
   （ 备注：uwgsi 启动 6001 端口、nginx 配置 6010 反向代理 6001 ）

5.本地相关服务的启动操作（ gulpfile.js 文件 ）
（1）启动服务并调试页面：gulp "html debug"
（2）停止服务命令：gulp "stop env"
（3）部署docker服务：gulp "deploy docker"


【 备 注 】
MAC本地安装的 nginx 相关路径
默认安装路径：/usr/local/Cellar/nginx/1.15.5/
默认配置文件路径：/usr/local/etc/nginx/
sudo nginx
sudo nginx -t
sudo nginx -s reload


【 虚拟环境添加依赖 】
1.创建虚拟环境：virtualenv -p /usr/local/bin/python3 venv （-p：指明python3所在目录）
2.切换到虚拟环境：source venv/bin/activate
3.退出虚拟环境：deactivate
4.添加依赖：
pip3 install -v flask==0.12 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


【 终端启动 appium desktop 服务命令 】
1.使用 appium desktop 时
    node /Applications/Appium.app/Contents/Resources/app/node_modules/appium/build/lib/main.js --port 4723
2.使用 appium server 时
    appium appium -a 127.0.0.1 -p 4723 --session-override &


------------------------------------------


【 本 地 配 置 Appium Android 环 境 】

1.adb连真机命令：adb connect 192.168.31.136:5555

2.启动appium服务命令：node /Applications/Appium.app/Contents/Resources/app/node_modules/appium/build/lib/main.js --port 4723

 （ 注：第一次需要在真机上进行授权、可能需要删除 ATX.apk 应用 ）


------------------------------------------

【 真 机 连 接 方 式 】

1.无线连接真机(使用一次USB)：
（1）通过USB将真机连接电脑
（2）让真机在5555端口监听TCP/IP连接：adb -s 设备ID tcpip 5555
（3）找到真机的ip地址：设置 -> 关于本机 -> 本机状态信息 -> IP地址
（4）通过ip地址连接真机：adb connect 192.168.31.56:5555
    （ 断开连接设备：adb disconnect 192.168.31.56:5555 ）

2.无线连接真机(无需USB)：
  前提：先将真机刷机获取root权限（ 通过win上使用'奇兔刷机'软件）
       在真机上安装超级终端模拟器（ Terminal_Emulator.apk ）：adb install Terminal_Emulator.apk
（1）使用真机在终端模拟器上输入下面两行
     su
     setprop service.adb.tcp.port 5555
     备注：有些设备（小米 5S）可能需要重启adbd服务：restart adbd（ 若无效 则：先 stop adbd  再 start adbd ）
（2）找到 设备的ip地址：设置 -> 关于本机 -> 本机状态信息 -> IP地址
（3）通过ip地址连接设备：adb connect 192.168.31.136:5555

------------------------------------------

【 Android 管理工具 ADB 命令 】

查看设备：adb devices

查看adb版本：adb version

停止adb服务：adb kill-server

查看某设备的屏幕分辨率：adb -s xxxxx shell wm size

查看设备包含的应用程序
（1）查看所有应用：adb -s 192.168.31.56:5555 shell pm list packages
（2）查看淘宝应用：adb -s 192.168.31.56:5555 shell pm list packages | grep taobao

安装/卸载应用：
（1）安装（应用宝）：adb -s 192.168.31.136:5555 install yyb.apk
（2）卸载（应用宝）：adb -s 192.168.31.136:5555 uninstall < packagename >
                    package: name='com.tencent.android.qqdownloader'
                    launchable-activity: name='com.tencent.pangu.link.SplashActivity'

清除应用数据与缓存:
adb -s 192.168.31.56:5555 shell pm clear < packagename >

查看应用正在运行services
adb -s 192.168.31.56:5555 shell dumpsys activity services < packagename >

查看应用详细信息:
adb -s 192.168.31.56:5555 shell dumpsys package < packagename >

唤醒设备屏幕：
adb -s 15a6c95a shell input keyevent 26




########################################################################################################################


【 Docker Centos7 相关 】


【 服 务 端 配 置 Appium Android 环 境 】

备注：
    生产环境为了减少意外情况，尽量使用无线连接真机
    使用无线连接真机，则需要确保 Docker环境 与 真机 处于同一个网络下

未解决的问题：
    'Docker'中无法获取通过'USB'连接的真机设备

环境配置 方案一：
    若 有些监控的真机无法获取root权限(刷机失败)
    则 在 linux 上启动一个容器：监控服务(Docker)
       在 win10 | mac_mini 上安装两个服务：Android-SDK、appium服务

    无线连接设备（需使用一次USB）
    （1）绑定真机 ：adb connect 192.168.31.136:5555
    （2）查看设备 ：adb devices
    （3）安装待测试apk ：adb -s 192.168.31.136:5555 install yyb.apk

环境配置 方案二：
    若 待监控的真机全部都可以获取root权限(刷机成功)
    则 在 linux | win10 | mac_mini 上启用两个容器：监控服务(Docker)、Appium服务(Docker) - budtmo/docker-android-real-device
      ( 备注：若 使用 linux 则要确保 linux 与 手机 处于同一网络 )

    无线连接设备(Docker）
    （1）绑定真机（不进入容器）：docker exec -it appium_andriod adb connect 192.168.31.136:5555
    （2）查看设备（不进入容器）：docker exec -it appium_andriod adb devices
    （3）安装待测试apk（不进入容器）：docker exec -it appium_andriod adb -s 192.168.31.136:5555 install yyb.apk

    Appium服务(Docker)中提供的'noVNC'界面地址来查看'appium log'
    http://docker_ip:6080

------------------------------------------


1.uWSGI配置文件：vassals_docker/app_uwsgi.ini
（1）启动 uWSGI 命令 在 ./start_uwsgi.sh 脚本
（2）停止 uWSGI 命令 在 ./stop_uwsgi.sh 脚本

2.服务器目录结构
  /var/log/uwsgi/ 		   -> pid_uwsgi.pid、app_uwsgi.log、emperor.log
  /var/log/nginx/ 		   -> error.log、access.log
  /etc/uwsgi/vassals/	   -> app_uwsgi.ini
  /opt/project/logs/ 	   -> 项目日志
  /opt/project/reports/	   -> 测试报告
  /opt/project/${pro_name} -> 项目
  /opt/project/tmp         -> 临时目录(部署时使用)

3.服务器部署命令：
（1）从GitGub上拉取代码至临时目录
（2）关闭nginx、mongo、uwsgi服务
（3）替换项目、uwsgi.ini配置文件
（4）替换env_config配置文件
（5）启动nginx、mongo、uwsgi服务
（6）清空临时文件

4.部署时的存放位置：
（1）./pythonSelenium -> /opt/project/pythonSelenium
（2）./pythonSelenium/vassals/app_uwsgi.ini -> /etc/uwsgi/vassals/app_uwsgi.ini

5.部署时相关配置文件的替换操作：
（1）将./Env/目录下的 env_config.py 删除
（2）将./Env/目录下的 env_config_docker.py 重命名为 env_config.py

6.访问地址（ Docker 内部 ）：
（1）测试报告 -> http://127.0.0.1:80/test_report/<pro_name>/[APP_report]<pro_name>.html
（2）接口地址 -> http://127.0.0.1:80/api/
               http://127.0.0.1:80/api/WEB/sync_run_case
               http://127.0.0.1:80/api/WEB/get_img/5e5cac9188121299450740b3
    ( 备注：uwgsi 启动 8081 端口、nginx 配置 80 反向代理 8081 )

7.访问地址（ 外部访问 ）：
（1）用例页面 -> http://192.168.31.10:1080/api/WEB/index
（2）测试报告 -> http://192.168.31.10:1080/test_report/<pro_name>/[WEB_report]<pro_name>.html
（3）接口地址 -> http://192.168.31.10:1080/api/
               http://192.168.31.10:1080/api/WEB/sync_run_case
               http://192.168.31.10:1080/api/WEB/get_img/5e5cac9188121299450740b3
    ( 备注：docker 配置 1080 映射 80 )

8.关于部署
  通过'fabric'工具进行部署 -> deploy.py
    （1）将本地代码拷贝入临时文件夹，并删除不需要的文件目录
    （2）将临时文件夹中的该项目压缩打包，上传至服务器的临时文件夹中
    （3）在服务器中进行部署操作：停止nginx、mongo、uwsgi服务 -> 替换项目、uwsgi.ini配置文件 -> 替换config配置文件 -> 启动nginx、mongo、uwsgi服务
    （4）删除本地的临时文件夹
  'gulp'命令 执行 deploy.py 文件 进行部署



########################################################################################################################

【 框 架 工 具 】
 Python3 + Selenium3 + unittest + Flask + uWSGI + Nginx + Bootstrap + MongoDB + Docker + Fabric + Gulp


【 框 架 结 构 】（ 提高代码的：可读性、重用性、易扩展性 ）
 1.Api层：       对外接口、原静态文件
 2.Build层：     编译后的静态文件
 3.Common层：    通用方法、测试方法
 4.Config层：    错误码映射、全局变量、定时任务、项目配置、测试地址配置
 5.Data层：      相关测试数据
 6.Env层：       环境配置
 7.Project层：   区分不同项目、page_object(页面操作方法、元素定位)、test_case(测试用例)
 8.TestBase层：  封装了浏览器驱动操作方法、提供'测试用例'父类第基础方法(继承’unittest.TestCase')、测试报告生成、同步执行用例方法
 9.Tools层：     工具函数
 10.其他：
 （1）vassals/ -> 服务器的'uWSGI配置'
 （2）vassals_local/、venv/ -> 本地的'uWSGI配置、python3虚拟环境'
 （3）Logs/、Reports/、Screenshot/ -> 临时生产的 日志、报告、截图
 （4）node_modules/、gulpfile.js、package.json、package-lock.json -> 供本地启动使用的gulp工具
 （5）deploy.py、start_uwsgi_local.sh、stop_uwsgi_local.sh、tmp_uwsgi_pid.txt -> 本地部署文件及相关命令和临时文件

【 功 能 点 】

1.使用 Python3 + Selenium3 + unittest + Bootstrap:
（1）使用'unittest'作为测试用例框架
（2）通过动态修改和添加'unittest.TestSuite'类中的方法和属性，实现启用多线程同时执行多条测试用例
（3）通过修改'HTMLTestRunner'文件并结合'unittest'测试框架，优化了测试报告的展示方式，并提供了每个测试用例的截图显示
（4）所有用例执行后，若有'失败'或'错误'的用例，则发送钉钉和邮件通知
（5）提供日志记录功能：按照日期区分
（6）提供定时任务：定时删除过期(一周前)的文件：日志、报告、截图文件(mongo数据)，定时执行测试用例
（7）提供页面展示项目用例，实现用例上下线、批量执行用例、显示报告、用例运行进度等功能

2.使用 Flask ：
（1）提供 执行用例的接口
（2）提供 获取截图的接口：供测试报告页面调用

3.使用 Nginx ：
（1）提供测试报告的查看地址
（2）反向代理相关接口、解决测试报告调用'获取截图接口'时的跨域访问问题

4.使用 uWSGI :
（1）用作 web 服务器
（2）使用'emperor'命令进行管理：监视和批量启停 vassals 目录下 uwsgi 相关的 .ini 文件

5.使用 Docker：
（1）使用Dockerfile构建centos7镜像：提供项目所需的相关配置环境
（2）使用'selenium/hub'和'selenium/node-chrome-debug'镜像，搭建'Selenium Grid'分布式测试环境
     （ 可以在linux中启动无界面浏览器测试，并可以指定浏览器的分辨率和实例个数，可以通过'VNC'连接进行调试）
（3）使用'docker-compose' 一键管理多个容器

6.使用 MongoDB ：
（1）使用'GridFS'进行图片文件的保存与读取

7.使用 Fabric ：
（1）配置相关脚本，实现一键部署

8.使用 NodeJS 的 Gulp 命令 ：
（1）配置本地启动的相关服务，实现一键启动或停止
（2）编译静态文件，防止浏览器缓存js问题
（3）实时监听本地调试页面功能

