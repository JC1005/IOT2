from azureml.core.workspace import Workspace
import configparser


class machineLearning:
    def __init__(self):
        configFilePath = "credentials/azure.ini"
        self.azureConfig = configparser.ConfigParser()
        try:
            self.azureConfig.read(configFilePath)
            self.ws = Workspace(
                subscription_id=self.azureConfig["default"]["subscription_id"],
                resource_group=self.azureConfig["default"]["resource_group"],
                workspace_name=self.azureConfig["default"]["workspace_name"],
            )
        except:
            print("Azure config file not found at " + configFilePath)
            print("A template will be provided.")
            self.azureConfig["default"] = {
                "subscription_id": "paste your subscription ID here",
                "resource_group": "paste your resource group here",
                "workspace_name": "paste your workspace name here",
            }
            with open(configFilePath, "w") as configfile:
                self.azureConfig.write(configfile)


if __name__ == "__main__":
    ml = machineLearning()
