import sys
import yaml

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    if len(sys.argv) < 2:
        print("Usage: python test.py <config_path>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_config(config_path)

    print("Printing configuration values:")
    for k, v in config.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
