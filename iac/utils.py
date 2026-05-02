from json import load
import sys


def get_config(env):
    if env is None:
        print("La variable de entorno ENVIRONMENT no esta definida.")
        print("Los valores posibles son: dev, testing y prod")
        print("Use export ENVIRONMENT=dev / testing / prod")
        sys.exit(1)

    if env not in ["dev", "testing", "prod"]:
        print("La variable de entorno ENVIRONMENT no tiene un valor valido")
        print(env)
        print("Los valores posibles son: dev, testing y prod")
        sys.exit(1)

    #  Load configurations file
    json_file = open(f"conf/{env}.json")
    conf_data = load(json_file)

    base_json_file = open(f"conf/base.json")
    base_conf_data = load(base_json_file)

    base_conf_data.update(conf_data)

    # print(base_conf_data)

    return base_conf_data


def create_dynamodb_arn(region, account, table_name):
    return f"arn:aws:dynamodb:{region}:{account}:table/{table_name}"
