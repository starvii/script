#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 最近有段时间python-pip无法安装。2020-05-10 kali暂时没有这种情况了
# 使用 wget https://bootstrap.pypa.io/get-pip.py
# python2 get-pip.py 安装pip
# huawei pypi源有问题，很多库没有。aliyun 暂时没发现不能安装的库


from __future__ import print_function
import os
import sys
from os import path


class _Do(object):
    order = 6

    @staticmethod
    def run(script, _=True): print(script)
    print_notice = print
    print_error = print

    def __init__(self):
        self.current_path = path.dirname(path.abspath(__file__))
        self.pip_conf = path.join(self.current_path, "pip.conf")
        self.script = """
################################################################################
cp {pip_conf} /root/.pip
################################################################################
apt install -y python python-pip
apt install -y python3 python3-pip
################################################################################
apt install -y libpython2-dev libpython3-all-dev libssl-dev libmpfr-dev libmpc-dev
python2 -m pip install -U pip setuptools -i {url}
python2 -m pip uninstall -y pycrypto
python2 -m pip install -U pycryptodome -i {url}
python2 -m pip install -U gmpy -i {url}
python2 -m pip install -U gmpy2 -i {url}
python2 -m pip install -U pwntools -i {url}
python3 -m pip install -U pip setuptools -i {url}
python3 -m pip uninstall -y pycrypto
python3 -m pip install -U pycryptodome -i {url}
python3 -m pip install -U gmpy -i {url}
python3 -m pip install -U gmpy2 -i {url}
python3 -m pip install -U uncompyle6 -i {url}
python3 -m pip install -U pwntools -i {url}
python3 -m pip install -U requests -i {url}
python3 -m pip install -U aiohttp -i {url}
python3 -m pip install -U lxml -i {url}
python3 -m pip install -U beautifulsoup4 -i {url}
python3 -m pip install -U tornado -i {url}
################################################################################
    """.format(url="https://mirrors.aliyun.com/pypi/simple", pip_conf=self.pip_conf)

    def do(self):
        _Do.run(self.script)


if "INIT_SCRIPT_BASE" in os.environ:
    INIT_SCRIPT_BASE = os.getenv("INIT_SCRIPT_BASE")
    sys.path.append("{}/_task_".format(INIT_SCRIPT_BASE))
    SuperTask = __import__("task".format(INIT_SCRIPT_BASE)).AbstractTask
    def init_func(self): self._action = _Do()
    _Do.run = SuperTask.run
    _Do.print_notice = SuperTask.print_notice
    _Do.print_error = SuperTask.print_error

    # 动态创建类
    _ = type("TaskAptInstallPython", (SuperTask,), dict(
        order=_Do.order,
        __init__=init_func
    ))


def main():
    action = _Do()
    action.do()


if __name__ == "__main__":
    main()
