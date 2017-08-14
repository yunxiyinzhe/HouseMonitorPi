# HouseMonitorPi
树莓派搭建的家庭环境监控系统，可以监测室内温湿度，室内空气质量，甲醛浓度。除此之外，还加入了个人博客和基于Slack的树莓派聊天机器人。

## 依赖
基于树莓派官方系统Raspbian Jessie开发，pip install：
> flask
> flask_script
> flask_flatpages
> flask_paginate
> pyserial
> pandas
> slackbot

## 使用

### HouseMonitorPi

#### 1.和风天气API
在此处[和风天气][1]注册，获取API后替换widget_utils.py第6行。

#### 2.心知天气插件
在此处[心知天气][2]注册，获取天气插件代码后加入weather_forcast.html的iframe标签中。

### Pi_Robot

#### 1.Slack Bot
在此处[Slack][3]注册，添加Slack Bot后，在slackbot_settings.py添加API_TOKEN

#### 2.图灵机器人
在此处[tuling123][4]注册，添加图灵机器人后，在tuling.json添加key

### Blog
app/pages下的实例构建目录结构，并以Sample.markdown为模板撰写博客。

## 运行
> sudo manage.py runserver
> sudo python run.py

[1]:http://www.heweather.com/
[2]:https://www.seniverse.com/widget/more
[3]:https://slack.com/
[4]:http://www.tuling123.com/

