# utils/performance_engine.py

import time
import csv
from pathlib import Path


# ==========================================
# API PERFORMANCE MONITOR
# ==========================================
class APIPerformance:

    # SLA threshold for API response time validation (in seconds)
    API_THRESHOLD = 20

    @staticmethod
    def validate(response, api_name="API"):

        # Extract API response time from response metadata
        response_time = response.elapsed.total_seconds()

        # Print formatted API performance log
        print(
            f"\n {api_name} Response Time: "
            f"{response_time:.2f} sec"
        )

        # Performance grading based on response time buckets
        if response_time < 2:
            print(" Excellent API Performance")

        elif response_time < 5:
            print(" Good API Performance")

        elif response_time < 10:
            print(" Acceptable API Performance")

        else:
            print(" Slow API Performance")

        # Log performance metrics for trend analysis across runs
        PerformanceTrendLogger.log(
            layer="API",
            action=api_name,
            response_time=response_time,
        )

        # Enforce SLA threshold to fail test if API is too slow
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

    # SLA threshold for UI page load time validation (in seconds)
    UI_THRESHOLD = 15

    @staticmethod
    def measure_page_load(driver, page_name="Page"):

        # Capture navigation start timestamp from browser performance API
        navigation_start = driver.execute_script(
            "return window.performance.timing.navigationStart"
        )

        # Capture DOM completion timestamp from browser performance API
        dom_complete = driver.execute_script(
            "return window.performance.timing.domComplete"
        )

        # Calculate total page load time in seconds
        load_time = (
            dom_complete - navigation_start
        ) / 1000

        # Print UI performance metric for debugging and reporting
        print(
            f"\n {page_name} Load Time: "
            f"{load_time:.2f} sec"
        )

        # UI performance classification logic
        if load_time < 3:
            print(" Excellent UI Performance")

        elif load_time < 6:
            print(" Good UI Performance")

        elif load_time < 10:
            print(" Acceptable UI Performance")

        else:
            print(" Slow UI Performance")

        # Log UI performance data for historical trend tracking
        PerformanceTrendLogger.log(
            layer="UI",
            action=page_name,
            response_time=load_time,
        )

        # Assert UI performance SLA compliance
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

    # CSV file path for storing performance trend history
    LOG_FILE = "logs/performance_trend.csv"

    @staticmethod
    def log(layer, action, response_time):

        # Ensure logs directory exists before writing trend data
        Path("logs").mkdir(
            parents=True,
            exist_ok=True
        )

        # Check if CSV file already exists to decide header writing
        file_exists = Path(
            PerformanceTrendLogger.LOG_FILE
        ).exists()

        # Open CSV file in append mode for continuous logging
        with open(
            PerformanceTrendLogger.LOG_FILE,
            mode="a",
            newline="",
        ) as file:

            writer = csv.writer(file)

            # Write header only for first-time file creation
            if not file_exists:

                writer.writerow(
                    [
                        "Layer",
                        "Action",
                        "ResponseTime",
                    ]
                )

            # Append performance record row
            writer.writerow(
                [
                    layer,
                    action,
                    f"{response_time:.2f}",
                ]
            )

        # Console log for traceability of performance tracking
        print(
            f" Trend Logged -> "
            f"{layer} | {action} | "
            f"{response_time:.2f} sec"
        )