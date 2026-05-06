import allure

def attach_json(name, data):
    allure.attach(
        str(data),
        name=name,
        attachment_type=allure.attachment_type.JSON
    )

# attach_json("API Response", res.json())