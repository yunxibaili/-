import json
import os
import time
import cv2
import numpy as np
import yaml
from pathlib import Path
from PIL import Image
import io
from appium import webdriver
from appium.webdriver.webdriver import WebDriver


class KeywordExecutor:
    def __init__(self, config_file="config.yaml", images_dir="images", reports_dir="reports/screenshots"):
        self.config = self._load_config(config_file)
        self.images_dir = Path(images_dir)
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.driver: WebDriver = None
        self.results = []
        self._screenshot_count = 0

    def _load_config(self, config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def connect_appium(self):
        appium_config = self.config.get("appium", {})
        caps = self.config.get("capabilities", {})
        
        url = f"http://{appium_config.get('host', '127.0.0.1')}:{appium_config.get('port', 4723)}/wd/hub"
        
        self.driver = webdriver.Remote(url, desired_capabilities=caps)
        print(f"Appium connected: {url}")
        return self.driver

    def disconnect_appium(self):
        if self.driver:
            self.driver.quit()
            print("Appium disconnected")

    def _screenshot(self):
        if not self.driver:
            return None
        return self.driver.get_screenshot_as_png()

    def save_screenshot(self, name=None):
        if not self.driver:
            return None
        
        self._screenshot_count += 1
        filename = name or f"screenshot_{self._screenshot_count}"
        filepath = self.reports_dir / f"{filename}.png"
        
        screenshot_data = self._screenshot()
        if screenshot_data:
            with open(filepath, "wb") as f:
                f.write(screenshot_data)
            return str(filepath)
        return None

    def _find_image(self, template_path, threshold=None):
        if not self.driver:
            return None
        
        if threshold is None:
            threshold = self.config.get("capabilities", {}).get("imageMatchThreshold", 0.8)
        
        screenshot_data = self._screenshot()
        if not screenshot_data:
            return None
        
        screen = cv2.imdecode(np.frombuffer(screenshot_data, np.uint8), cv2.IMREAD_COLOR)
        template = cv2.imread(str(template_path))
        
        if template is None:
            return None
        
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y, max_val)
        return None

    def load_steps(self, steps_file):
        with open(steps_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def execute(self, step):
        keyword = step.get("keyword")
        
        keyword_handlers = {
            "start_app": self._start_app,
            "click_image": self._click_image,
            "click": self._click_image,
            "wait": self._wait,
            "exists": self._exists,
            "swipe": self._swipe,
            "input_text": self._input_text,
            "screenshot": self._screenshot_step,
            "click_coords": self._click_coords,
            "close_app": self._close_app,
        }
        
        handler = keyword_handlers.get(keyword)
        if handler:
            return handler(step)
        return {"status": "error", "message": f"Unknown keyword: {keyword}"}

    def _start_app(self, step):
        timeout = step.get("timeout", 30)
        if not self.driver:
            self.connect_appium()
        time.sleep(2)
        return {"status": "pass", "message": f"App started", "screenshot": self.save_screenshot("start_app")}

    def _close_app(self, step):
        if self.driver:
            self.driver.close_app()
        return {"status": "pass", "message": "App closed"}

    def _click_image(self, step):
        image = step.get("image")
        timeout = step.get("timeout", 10)
        threshold = step.get("threshold")
        
        image_path = self.images_dir / image
        if not image_path.exists():
            return {"status": "fail", "message": f"Image not found: {image}", "screenshot": self.save_screenshot("fail_click_image")}
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self._find_image(image_path, threshold)
            if result:
                x, y, confidence = result
                if self.driver:
                    self.driver.tap([(x, y)])
                return {"status": "pass", "message": f"Click {image} at ({x}, {y}), confidence: {confidence:.2f}", "image": image}
            time.sleep(1)
        
        return {"status": "fail", "message": f"Image not found within {timeout}s: {image}", "screenshot": self.save_screenshot(f"fail_{image}")}

    def _wait(self, step):
        seconds = step.get("seconds", 1)
        time.sleep(seconds)
        return {"status": "pass", "message": f"Wait {seconds}s"}

    def _exists(self, step):
        image = step.get("image")
        timeout = step.get("timeout", 30)
        threshold = step.get("threshold")
        
        image_path = self.images_dir / image
        if not image_path.exists():
            return {"status": "fail", "message": f"Image not found: {image}", "screenshot": self.save_screenshot("fail_exists")}
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self._find_image(image_path, threshold)
            if result:
                return {"status": "pass", "message": f"Image found: {image}", "image": image}
            time.sleep(1)
        
        return {"status": "fail", "message": f"Image not found within {timeout}s: {image}", "screenshot": self.save_screenshot(f"fail_exists_{image}")}

    def _swipe(self, step):
        start_x = step.get("start_x", 500)
        start_y = step.get("start_y", 1000)
        end_x = step.get("end_x", 500)
        end_y = step.get("end_y", 200)
        duration = step.get("duration", 500)
        
        if self.driver:
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        
        return {"status": "pass", "message": f"Swipe from ({start_x}, {start_y}) to ({end_x}, {end_y})"}

    def _input_text(self, step):
        text = step.get("text")
        element_id = step.get("element_id")
        
        if self.driver and element_id:
            elem = self.driver.find_element_by_id(element_id)
            elem.send_keys(text)
            return {"status": "pass", "message": f"Input text: {text}"}
        
        return {"status": "fail", "message": f"Input text failed: {text}"}

    def _screenshot_step(self, step):
        name = step.get("name", f"screenshot_{self._screenshot_count}")
        filepath = self.save_screenshot(name)
        return {"status": "pass", "message": f"Screenshot saved: {name}", "screenshot": filepath}

    def _click_coords(self, step):
        x = step.get("x")
        y = step.get("y")
        
        if self.driver and x and y:
            self.driver.tap([(x, y)])
            return {"status": "pass", "message": f"Click at ({x}, {y})"}
        
        return {"status": "fail", "message": f"Click coords failed: ({x}, {y})"}

    def run_test_case(self, test_case):
        name = test_case.get("name")
        steps = test_case.get("steps", [])
        results = {"name": name, "steps": [], "status": "pass", "screenshots": []}

        for i, step in enumerate(steps):
            result = self.execute(step)
            result["step_index"] = i + 1
            results["steps"].append(result)
            
            if result.get("screenshot"):
                results["screenshots"].append(result["screenshot"])
            
            if result["status"] == "fail":
                results["status"] = "fail"
                break

        return results

    def run_all(self, steps_data):
        test_cases = steps_data.get("test_cases", [])
        all_results = {"test_cases": [], "summary": {"total": 0, "pass": 0, "fail": 0, "skip": 0}}

        for test_case in test_cases:
            result = self.run_test_case(test_case)
            all_results["test_cases"].append(result)
            all_results["summary"]["total"] += 1
            if result["status"] == "pass":
                all_results["summary"]["pass"] += 1
            elif result["status"] == "skip":
                all_results["summary"]["skip"] += 1
            else:
                all_results["summary"]["fail"] += 1

        return all_results