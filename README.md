# 手游自动化测试框架

基于 Python + Appium + OpenCV 的关键字驱动自动化测试框架。

## 目录结构

```
game_auto_test/
├── config.yaml          # Appium 设备配置
├── steps.json          # 测试用例定义
├── executor.py         # 关键字执行引擎
├── runner.py           # 测试运行器 (含 pytest + Allure)
├── requirements.txt    # 依赖包
├── images/             # 图片素材目录
└── reports/            # 测试报告输出
    └── screenshots/    # 失败截图
```

## 安装

```bash
pip install -r requirements.txt
```

## 使用方式

### 1. 直接运行 (简单模式)
```bash
python runner.py
```

### 2. Pytest + Allure 模式
```bash
# 运行测试并生成 Allure 数据
pytest runner.py --alluredir=reports/allure -v

# 生成 Allure 报告
allure serve reports/allure
```

## 测试用例 (steps.json)

| 用例 | 说明 |
|------|------|
| TC001_登录流程 | 登录游戏账号 |
| TC002_战斗流程 | 开始战斗并验证胜利 |
| TC003_抽卡流程 | 十连抽卡 |
| TC004_商城购买 | 购买道具 |
| TC005_任务奖励 | 领取任务奖励 |

## 关键字支持

| 关键字 | 说明 | 参数 |
|--------|------|------|
| start_app | 启动应用 | timeout |
| click_image | 图像点击 | image, timeout, threshold |
| click | 同 click_image | image, timeout |
| wait | 等待 | seconds |
| exists | 图像存在检查 | image, timeout, threshold |
| swipe | 滑动 | start_x, start_y, end_x, end_y, duration |
| input_text | 输入文本 | text, element_id |
| screenshot | 截图 | name |
| click_coords | 坐标点击 | x, y |
| close_app | 关闭应用 | - |

## 配置 (config.yaml)

修改 `config.yaml` 中的设备连接参数：
- `host` / `port`: Appium 服务器地址
- `capabilities`: 设备能力配置 (platformName, deviceName, appPackage 等)

## 图片素材

将游戏截图放入 `images/` 目录，支持 PNG 格式。

## 报告

- JSON 报告: `reports/report_YYYYMMDD_HHMMSS.json`
- Allure 报告: `reports/allure/`
- 失败截图: `reports/screenshots/`