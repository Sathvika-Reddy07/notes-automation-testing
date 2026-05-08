#It helps us attach API responses or data into Allure reports for better analysis and debugging.
import allure

# Utility function to attach JSON data into Allure report
# used for debugging API responses in test reports
def attach_json(name, data):

    # Attach data as string in JSON format to Allure report
    allure.attach(
        str(data),
        name=name,
        attachment_type=allure.attachment_type.JSON
    )

# Example usage (commented):
# attach_json("API Response", res.json())