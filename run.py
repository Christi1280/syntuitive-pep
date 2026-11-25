import argparse

from app import create_app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SYNTUITIVE PEP locally.")
    parser.add_argument("--debug", action="store_true", help="Enable Flask debugging.")
    args = parser.parse_args()
    create_app(local=True).run(host="127.0.0.1", debug=args.debug, use_reloader=False)
