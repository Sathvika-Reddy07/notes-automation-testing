# utils/performance_engine.py

import time
import csv
from pathlib import Path


# ==========================================
# API PERFORMANCE MONITOR
# ==========================================
class APIPerformance:

    API_THRESHOLD = 20

    @staticmethod
    def validate(response, api_name="API"):

        response_time = response.elapsed.total_seconds()

        print(
            f"\n⚡ {api_name} Response Time: "
            f"{response_time:.2f} sec"
        )

        if response_time < 2:
            print("✅ Excellent API Performance")

        elif response_time < 5:
            print("✅ Good API Performance")

        elif response_time < 10:
            print("⚠️ Acceptable API Performance")

        else:
            print("❌ Slow API Performance")

        # trend logging
        PerformanceTrendLogger.log(
            layer="API",
            action=api_name,
            response_time=response_time,
        )

        assert (
            response_time < APIPerformance.API_THRESHOLD
        ), (
            f"{api_name} too slow: "
            f"{response_time:.2f} sec"
        )


# ==========================================
# UI PERFORMANCE MONITOR
# ==========================================
class UIPerformance:

    UI_THRESHOLD = 15

    @staticmethod
    def measure_page_load(driver, page_name="Page"):

        navigation_start = driver.execute_script(
            "return window.performance.timing.navigationStart"
        )

        dom_complete = driver.execute_script(
            "return window.performance.timing.domComplete"
        )

        load_time = (
            dom_complete - navigation_start
        ) / 1000

        print(
            f"\n🌐 {page_name} Load Time: "
            f"{load_time:.2f} sec"
        )

        if load_time < 3:
            print("✅ Excellent UI Performance")

        elif load_time < 6:
            print("✅ Good UI Performance")

        elif load_time < 10:
            print("⚠️ Acceptable UI Performance")

        else:
            print("❌ Slow UI Performance")

        # trend logging
        PerformanceTrendLogger.log(
            layer="UI",
            action=page_name,
            response_time=load_time,
        )

        assert (
            load_time < UIPerformance.UI_THRESHOLD
        ), (
            f"{page_name} load too slow: "
            f"{load_time:.2f} sec"
        )


# ==========================================
# PERFORMANCE TREND LOGGER
# ==========================================
class PerformanceTrendLogger:

    LOG_FILE = "logs/performance_trend.csv"

    @staticmethod
    def log(layer, action, response_time):

        Path("logs").mkdir(
            parents=True,
            exist_ok=True
        )

        file_exists = Path(
            PerformanceTrendLogger.LOG_FILE
        ).exists()

        with open(
            PerformanceTrendLogger.LOG_FILE,
            mode="a",
            newline="",
        ) as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow(
                    [
                        "Layer",
                        "Action",
                        "ResponseTime",
                    ]
                )

            writer.writerow(
                [
                    layer,
                    action,
                    f"{response_time:.2f}",
                ]
            )

        print(
            f"📊 Trend Logged -> "
            f"{layer} | {action} | "
            f"{response_time:.2f} sec"
        )