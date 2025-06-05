import sys
import yaml

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    if len(sys.argv) < 2:
        print("Usage: python test.py config.yam")
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_config(config_path)

    print("Printing configuration values:")
    for k, v in config.items():
        print(f"{k}: {v}")

    print("\n--- Individual Values ---")
    print(f"central_api_token: {config.get('central_api_token', 'N/A')}")
    print(f"serial_number: {config.get('serial_number', 'N/A')}")

if __name__ == "__main__":
    main()
