import subprocess
from zabbix_utils import ZabbixAPI  # ou pyzabbix
import os

api = ZabbixAPI(url="192.168.15.141")
api.login(user="Admin", password="zabbix")

git_archive_name = subprocess.run( ["git", "diff", "--name-only", "origin/master"], capture_output=True, text=True)
file_changed = git_archive_name.stdout.strip().splitlines()[0]


yaml_content = ''
with open(f"./{file_changed}", "r", encoding="utf-8") as f:
     yaml_content = f.read()

print(yaml_content)
# Requisição de importação
result = api.configuration.import_({
    "source": yaml_content,
    "format": "yaml",
    "rules": {
        "templates": {
            "createMissing": True,
            "updateExisting": True
        },
        "items": {
            "createMissing": True,
            "updateExisting": True,
            "deleteMissing": True
        },
        "triggers": {
            "createMissing": True,
            "updateExisting": True,
            "deleteMissing": True
        },
        "valueMaps": {
            "createMissing": True,
            "updateExisting": False
        }
    }})

print("Importação concluída:", result)


api.logout()