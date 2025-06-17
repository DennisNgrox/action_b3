import subprocess
from zabbix_utils import ZabbixAPI  # ou pyzabbix
import os

ZABBIX_PASSWORD = os.getenv('ZABBIX_TOKEN')
api = ZabbixAPI(url="https://zabbix.ageri.com.br/")
api.login(token={ZABBIX_PASSWORD})

git_archive_name = subprocess.run(["git", "diff", "--name-only", "HEAD@{1}", "HEAD", "--relative", "templates/"], capture_output=True, text=True)
changed_files = [file.strip() for file in git_archive_name.stdout.splitlines() if file.strip()]

print("Arquivos modificados no último push:")
print("\n".join(changed_files))

for i in changed_files:
    yaml_content = ''
    with open(f"./{i}", "r", encoding="utf-8") as f:
        yaml_content = f.read()

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

