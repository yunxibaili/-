import json
import sys
from datetime import datetime
from pathlib import Path

from executor import KeywordExecutor


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
    runner = TestRunner()
    runner.run()