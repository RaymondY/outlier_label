"""
    render_template 是渲染模板用的，这里我们用来返回 index.html
    flask_cors 用来解决跨域的问题
"""
import os
import traceback
import numpy as np
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# 通过 static_folder 指定静态资源路径，以便 index.html 能正确访问 CSS 等静态资源
# template_folder 指定模板路径，以便 render_template 能正确渲染 index.html
app = Flask(__name__, static_folder='./templates/static', template_folder='./templates')

CORS(app, supports_credentials=True)
data = None


def loadData(path, metric_num, input_size, day_num):
    temp_data = np.loadtxt(path, skiprows=1, delimiter=',')
    data = np.zeros(shape=(metric_num, input_size * day_num))
    for kpi in range(metric_num):
        # baseline 预留 可以raw_data做预处理
        baseline = temp_data[:, kpi]
        data[kpi] = baseline

    # row: kpi(19); col: 288*15/test, 288*30/train
    return data


@app.route("/")
def index():
    """
        当在浏览器访问网址时，通过 render_template 方法渲染 dist 文件夹中的 index.html。
        页面之间的跳转交给前端路由负责，后端不用再写大量的路由
    """
    return render_template('index.html')


# 上传文件
@app.route("/upload", methods=['POST'])
def upload():
    # noinspection PyBroadException
    try:
        file_name = request.data.decode("utf-8")
        path = "./data/" + file_name
        # 应该在前端留接口
        metric_num, input_size, day_num = 19, 288, 15
        global data
        data = loadData(path, metric_num, input_size, day_num)
        message = {'status': 'success'}
        # return jsonify(message)
        return jsonify(data.tolist())
    except Exception as e:
        traceback.print_exc()
        return jsonify({'status': 'fail'})


@app.route('/get', methods=['GET'])
def get_data():
    global data
    # noinspection PyBroadException
    try:
        response_data = data.tolist()
        return jsonify(response_data)

    except Exception as e:
        traceback.print_exc()

        return None


if __name__ == '__main__':
    # 开启 debug模式，这样我们就不用每更改一次文件，就重新启动一次服务
    # 设置 host='0.0.0.0'，让操作系统监听所有公网 IP
    # 也就是把自己的电脑作为服务器，可以让别人访问
    # app.run(debug=True)
    app.run(debug=False)
