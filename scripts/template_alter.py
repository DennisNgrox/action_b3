import subprocess
from zabbix_utils import ZabbixAPI  # ou pyzabbix
import os
import logging

# Configuração do logging para mostrar mensagens no GitHub Actions
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 1. Debug inicial
logger.info("=== Iniciando script ===")
logger.info(f"TOKEN_ZABBIX definido? {'Sim' if os.getenv('TOKEN_ZABBIX') else 'Não'}")

# 2. Verifica o token
ZABBIX_TOKEN = os.getenv('TOKEN_ZABBIX')
if not ZABBIX_TOKEN:
    logger.error("❌ TOKEN_ZABBIX não encontrado nas variáveis de ambiente!")
    exit(1)

# 3. Conexão com a API do Zabbix
try:
    api = ZabbixAPI(url="https://zabbix.ageri.com.br/")
    api.login(token=ZABBIX_TOKEN)
    logger.info("Conectado à API do Zabbix com sucesso!")
except Exception as e:
    logger.error(f"❌ Falha na conexão com o Zabbix: {e}")
    exit(1)

# 4. Lista arquivos modificados
try:
    logger.info("Executando git diff...")
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD", "--relative", "templates/"],
        capture_output=True,
        text=True
    )
    logger.info(f"Saída do git diff: {result.stdout}")
    changed_files = [file.strip() for file in result.stdout.splitlines() if file.strip()]
except Exception as e:
    logger.error(f"❌ Erro ao executar git diff: {e}")
    exit(1)

# 5. Processa cada arquivo
for file_path in changed_files:
    try:
        logger.info(f"Processando: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
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

        logger.info(f"Importação concluída: {result}")
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar {file_path}: {e}")