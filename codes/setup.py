#!/usr/bin/env python3
from setuptools import setup

setup(
    name="binance-futures",
    version="1.1.0",
    packages=['binance_f', 'binance_f.impl', 'binance_f.impl.utils', 'binance_f.exception', 'binance_f.model', 'binance_f.base', 'binance_f.constant', 'binance_d', 'binance_d.impl', 'binance_d.impl.utils', 'binance_d.exception', 'binance_d.model', 'binance_d.base', 'binance_d.constant'],
    install_requires=['requests', 'apscheduler', 'websocket-client', 'urllib3', 'tzlocal<3.0']
)

