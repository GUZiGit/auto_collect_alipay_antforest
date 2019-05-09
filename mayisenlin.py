# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from airtest.core.api import *


def unlock_device(dev):
    """
    解锁设备(图案锁屏)
    :param dev: 连接的设备
    :return:
    """
    dev.shell('input keyevent 26')
    swipe((100, 400), vector=[-0.0149, -0.9193])

    dev.minitouch.swipe_along(
        [[0, 0]])


def collect_energy(is_home=False):
    """
    收取能量，自己的和好友的
    :param is_home: 是否是自己的
    :return:
    """
    if is_home:

        if not exists(Template(r"data/mayisenlin/tpl1557374412969.png", record_pos=(0.32, -0.203), resolution=(1080, 1920))):
            return

        energy_list = find_all(Template(r"data/mayisenlin/tpl1557374412969.png", record_pos=(0.32, -0.203), resolution=(1080, 1920)))
    else:
        if exists(Template(r"data/mayisenlin/tpl1557373442966.png", record_pos=(-0.062, -0.566), resolution=(1080, 1920))):
            return
        energy_list = find_all(Template(r"data/mayisenlin/tpl1557370999417.png", record_pos=(0.034, -0.215), resolution=(1080, 1920)))

    if not energy_list:
        return
    for energy in energy_list:
        if is_home:
            touch(energy["result"])
        else:
            touch((energy["result"][0], energy["result"][1] - 10))


def find_friends_energy():
    """
    判断好友列表中是否有能量可以收取，如果发现有就收取
    :return:
    """
    energy_friends = find_all(Template(r"data/mayisenlin/tpl1557371179958.png", record_pos=(0.475, 0.15), resolution=(1080, 1920)))
    if not energy_friends:
        return
    for friend in energy_friends:
        touch(friend["result"])
        sleep(1)
        collect_energy()
        touch(Template(r"data/mayisenlin/tpl1557373711838.png", record_pos=(-0.443, -0.765), resolution=(1080, 1920)))


def start_alipy_forest(dev):
    """
    启动支付宝，并且打开蚂蚁森林，前提是蚂蚁森林在支付宝首页
    :param dev: 连接的设备
    :return:
    """
    package = 'com.eg.android.AlipayGphone'
    dev.stop_app(package)
    dev.start_app(package)
    wait(Template(r"data/mayisenlin/tpl1557371626529.png", record_pos=(-0.37, -0.141), resolution=(1080, 1920)))
    touch(Template(r"data/mayisenlin/tpl1557371626529.png", record_pos=(-0.37, -0.141), resolution=(1080, 1920)))
    sleep(1)
    wait(Template(r"data/mayisenlin/tpl1557372598598.png", record_pos=(-0.344, -0.759), resolution=(1080, 1920)))


def swipe_next(check_more=True):
    """
    滑动界面
    :param check_more: 查看更多好友
    :return:
    """
    find_friends_energy()
    if check_more:
        result = exists(
            Template(r"data/mayisenlin/tpl1557374693373.png", threshold=0.86, record_pos=(0.062, -0.115), resolution=(1080, 1920)))
        if result:
            check_more = False
            touch(result)
    if exists(Template(r"data/mayisenlin/tpl1557371700856.png", threshold=0.85, record_pos=(0.012, 0.819), resolution=(1080, 1920))):
        return
    look_more_result = exists(
        Template(r"data/mayisenlin/tpl1557379057683.png", threshold=0.85, record_pos=(0.005, 0.845), resolution=(1080, 1920)))
    if look_more_result:
        touch(look_more_result)
    swipe((100, 500), vector=[0, -0.99])
    return swipe_next(check_more=check_more)


def main():
    dev = connect_device('Android://127.0.0.1:5037/XXX')  # 填写自己的设备号
    if dev.is_locked():
        unlock_device(dev)
    start_alipy_forest(dev)
    collect_energy(is_home=True)
    swipe_next()
    dev.shell('input keyevent 26')


if __name__ == "__main__":
    main()
