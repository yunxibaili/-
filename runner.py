import json
import os
import sys
from datetime import datetime
from pathlib import Path

import allure
import pytest

from executor import KeywordExecutor


class TestGameAuto:
    @classmethod
    def setup_class(cls):
        cls.executor = KeywordExecutor(
            config_file="config.yaml",
            images_dir="images",
            reports_dir="reports/screenshots"
        )
    
    @classmethod
    def teardown_class(cls):
        cls.executor.disconnect_appium()

    def run_test_from_json(self):
        steps_data = self.executor.load_steps("steps.json")
        return self.executor.run_all(steps_data)


@allure.feature("游戏自动化测试")
class TestGameLogin:
    @classmethod
    def setup_class(cls):
        cls.executor = KeywordExecutor(
            config_file="config.yaml",
            images_dir="images",
            reports_dir="reports/screenshots"
        )

    @classmethod
    def teardown_class(cls):
        cls.executor.disconnect_appium()

    @allure.story("登录流程")
    @allure.title("TC001 - 登录流程测试")
    def test_login(self):
        steps_data = self.executor.load_steps("steps.json")
        test_cases = steps_data.get("test_cases", [])
        
        login_case = next((tc for tc in test_cases if tc["name"] == "TC001_登录流程"), None)
        
        if not login_case:
            pytest.skip("Login test case not found")
        
        with allure.step("执行登录步骤"):
            result = self.executor.run_test_case(login_case)
        
        for step_result in result.get("steps", []):
            step_name = step_result.get("message", f"Step {step_result.get('step_index')}")
            with allure.step(step_name):
                if step_result.get("screenshot"):
                    allure.attach.file(
                        step_result["screenshot"],
                        name=step_name,
                        attachment_type=allure.attachment_type.PNG
                    )
            
            if step_result["status"] == "fail":
                pytest.fail(f"Step failed: {step_name} - {step_result.get('message')}")
        
        assert result["status"] == "pass", f"Login test failed: {result}"


@allure.feature("游戏自动化测试")
class TestGameBattle:
    @classmethod
    def setup_class(cls):
        cls.executor = KeywordExecutor(
            config_file="config.yaml",
            images_dir="images",
            reports_dir="reports/screenshots"
        )

    @classmethod
    def teardown_class(cls):
        cls.executor.disconnect_appium()

    @allure.story("战斗流程")
    @allure.title("TC002 - 战斗流程测试")
    def test_battle(self):
        steps_data = self.executor.load_steps("steps.json")
        test_cases = steps_data.get("test_cases", [])
        
        battle_case = next((tc for tc in test_cases if tc["name"] == "TC002_战斗流程"), None)
        
        if not battle_case:
            pytest.skip("Battle test case not found")
        
        with allure.step("执行战斗步骤"):
            result = self.executor.run_test_case(battle_case)
        
        for step_result in result.get("steps", []):
            step_name = step_result.get("message", f"Step {step_result.get('step_index')}")
            with allure.step(step_name):
                if step_result.get("screenshot"):
                    allure.attach.file(
                        step_result["screenshot"],
                        name=step_name,
                        attachment_type=allure.attachment_type.PNG
                    )
            
            if step_result["status"] == "fail":
                pytest.fail(f"Step failed: {step_name} - {step_result.get('message')}")
        
        assert result["status"] == "pass", f"Battle test failed: {result}"


@allure.feature("游戏自动化测试")
class TestGameGacha:
    @classmethod
    def setup_class(cls):
        cls.executor = KeywordExecutor(
            config_file="config.yaml",
            images_dir="images",
            reports_dir="reports/screenshots"
        )

    @classmethod
    def teardown_class(cls):
        cls.executor.disconnect_appium()

    @allure.story("抽卡流程")
    @allure.title("TC003 - 抽卡流程测试")
    def test_gacha(self):
        steps_data = self.executor.load_steps("steps.json")
        test_cases = steps_data.get("test_cases", [])
        
        gacha_case = next((tc for tc in test_cases if tc["name"] == "TC003_抽卡流程"), None)
        
        if not gacha_case:
            pytest.skip("Gacha test case not found")
        
        with allure.step("执行抽卡步骤"):
            result = self.executor.run_test_case(gacha_case)
        
        for step_result in result.get("steps", []):
            step_name = step_result.get("message", f"Step {step_result.get('step_index')}")
            with allure.step(step_name):
                if step_result.get("screenshot"):
                    allure.attach.file(
                        step_result["screenshot"],
                        name=step_name,
                        attachment_type=allure.attachment_type.PNG
                    )
            
            if step_result["status"] == "fail":
                pytest.fail(f"Step failed: {step_name} - {step_result.get('message')}")
        
        assert result["status"] == "pass", f"Gacha test failed: {result}"


@allure.feature("游戏自动化测试")
class TestGameShop:
    @classmethod
    def setup_class(cls):
        cls.executor = KeywordExecutor(
            config_file="config.yaml",
            images_dir="images",
            reports_dir="reports/screenshots"
        )

    @classmethod
    def teardown_class(cls):
        cls.executor.disconnect_appium()

    @allure.story("商城流程")
    @allure.title("TC004 - 商城购买测试")
    def test_shop(self):
        steps_data = self.executor.load_steps("steps.json")
        test_cases = steps_data.get("test_cases", [])
        
        shop_case = next((tc for tc in test_cases if tc["name"] == "TC004_商城购买"), None)
        
        if not shop_case:
            pytest.skip("Shop test case not found")
        
        with allure.step("执行商城购买步骤"):
            result = self.executor.run_test_case(shop_case)
        
        for step_result in result.get("steps", []):
            step_name = step_result.get("message", f"Step {step_result.get('step_index')}")
            with allure.step(step_name):
                if step_result.get("screenshot"):
                    allure.attach.file(
                        step_result["screenshot"],
                        name=step_name,
                        attachment_type=allure.attachment_type.PNG
                    )
            
            if step_result["status"] == "fail":
                pytest.fail(f"Step failed: {step_name} - {step_result.get('message')}")
        
        assert result["status"] == "pass", f"Shop test failed: {result}"


@allure.feature("游戏自动化测试")
class TestGameTask:
    @classmethod
    def setup_class(cls):
        cls.executor = KeywordExecutor(
            config_file="config.yaml",
            images_dir="images",
            reports_dir="reports/screenshots"
        )

    @classmethod
    def teardown_class(cls):
        cls.executor.disconnect_appium()

    @allure.story("任务流程")
    @allure.title("TC005 - 任务奖励领取测试")
    def test_task(self):
        steps_data = self.executor.load_steps("steps.json")
        test_cases = steps_data.get("test_cases", [])
        
        task_case = next((tc for tc in test_cases if tc["name"] == "TC005_任务奖励领取"), None)
        
        if not task_case:
            pytest.skip("Task test case not found")
        
        with allure.step("执行任务奖励领取步骤"):
            result = self.executor.run_test_case(task_case)
        
        for step_result in result.get("steps", []):
            step_name = step_result.get("message", f"Step {step_result.get('step_index')}")
            with allure.step(step_name):
                if step_result.get("screenshot"):
                    allure.attach.file(
                        step_result["screenshot"],
                        name=step_name,
                        attachment_type=allure.attachment_type.PNG
                    )
            
            if step_result["status"] == "fail":
                pytest.fail(f"Step failed: {step_name} - {step_result.get('message')}")
        
        assert result["status"] == "pass", f"Task test failed: {result}"


class TestRunner:
    def __init__(self, steps_file="steps.json", images_dir="images", reports_dir="reports"):
        self.steps_file = steps_file
        self.images_dir = images_dir
        self.reports_dir = Path(reports_dir)
        self.screenshots_dir = self.reports_dir / "screenshots"
        self.executor = KeywordExecutor(
            config_file="config.yaml",
            images_dir=images_dir,
            reports_dir=str(self.screenshots_dir)
        )
        self.reports_dir.mkdir(exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)

    def run(self):
        print("=" * 50)
        print("Game Auto Test Started")
        print("=" * 50)

        steps_data = self.executor.load_steps(self.steps_file)
        results = self.executor.run_all(steps_data)

        self._print_results(results)
        self._save_report(results)

        return results

    def _print_results(self, results):
        summary = results["summary"]
        print(f"\nTotal: {summary['total']}")
        print(f"Pass: {summary['pass']}")
        print(f"Fail: {summary['fail']}")
        print(f"Skip: {summary['skip']}")
        print("=" * 50)

        for tc in results["test_cases"]:
            status_icon = {"pass": "✓", "fail": "✗", "skip": "-"}
            icon = status_icon.get(tc["status"], "?")
            print(f"{icon} {tc['name']}: {tc['status']}")

    def _save_report(self, results):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"report_{timestamp}.json"

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\nReport saved: {report_file}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        print("Running with pytest...")
        pytest.main([__file__, "--alluredir=reports/allure", "-v"])
    else:
        runner = TestRunner()
        runner.run()