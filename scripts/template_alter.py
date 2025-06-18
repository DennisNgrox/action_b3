import sys
from zabbix_utils import ZabbixAPI
import os
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("=== Iniciando script ===")
        
        ZABBIX_TOKEN = os.getenv('TOKEN_ZABBIX')
        if not ZABBIX_TOKEN:
            raise ValueError("Token do Zabbix não encontrado")
        logger.info("TOKEN_ZABBIX definido: Sim")

        logger.info("Conectando à API do Zabbix...")
        api = ZabbixAPI(url="https://zabbix.ageri.com.br/")
        api.login(token=ZABBIX_TOKEN)
        logger.info("Conectado à API do Zabbix com sucesso!")

        if len(sys.argv) < 2:
            raise ValueError("Nenhum arquivo para processar")
        
        changed_files = sys.argv[1].split()
        logger.info(f"Arquivos a processar: {changed_files}")

        for file_path in changed_files:
            try:
                logger.info(f"Processando: {file_path}")
                
                with open(file_path, "r", encoding="utf-8") as f:
                    yaml_content = f.read()

                logger.info("Importando para o Zabbix...")
                result = api.configuration.import_({
                    "source": yaml_content,
                    "format": "yaml",
                    "rules": {
                        "templates": {"createMissing": True, "updateExisting": True},
                        "items": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
                        "triggers": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
                        "valueMaps": {"createMissing": True, "updateExisting": False}
                    }
                })
                logger.info(f"Importação concluída: {result}")

            except Exception as e:
                logger.error(f"Erro ao processar {file_path}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    logger.info("=== Script finalizado ===")