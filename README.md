# 手游抽卡自动化测试框架

基于 Python + Appium + OpenCV 的简单抽卡测试框架。

## 目录结构

```
game_auto_test/
├── config.yaml      # Appium 设备配置
├── steps.json     # 测试用例 (抽卡)
├── executor.py    # 关键字执行引擎
├── runner.py       # 测试运行器
├── requirements.txt # 依赖包
├── images/        # 图片素材
│   ├── gacha_btn.png
│   └── draw_btn.png
└── reports/       # 测试报告
    └── screenshots/
```

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python runner.py
```

## 配置

修改 `config.yaml` 中的 Appium 连接参数和游戏包名。

## 报告

JSON 报告保存在 `reports/report_YYYYMMDD_HHMMSS.json`