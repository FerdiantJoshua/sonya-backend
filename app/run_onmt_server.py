import os

from question_generator.api.config import API_CONFIG

def main():
    ip = API_CONFIG['onmt_server_host']
    port = API_CONFIG['onmt_server_port']
    url_root = API_CONFIG['onmt_server_url_root']
    config_file_path = API_CONFIG['onmt_server_config']

    command = f"onmt_server --ip={ip} --port={port} --url_root={url_root} --config={config_file_path}"
    print(command)
    os.system(command)

if __name__ == '__main__':
    main()
