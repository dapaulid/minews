import os
from datetime import datetime

def save_file(filename, data):
    ext = os.path.splitext(filename)[-1]
    if ext == '.yaml':
        import yaml
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    elif ext == '.md':
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
    else:
        raise ValueError("Unsupported file format: %s" % filename)
    # end if

def load_file(filename):
    ext = os.path.splitext(filename)[-1]
    if ext == '.yaml':
        import yaml
        with open(filename, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    elif ext == '.md':
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError("Unsupported file format: %s" % filename)
    # end if

# searches for the file with given name in the current directory and parent directories
def locate_file(basename) -> str:
    current_dir = os.path.abspath(os.getcwd())
    while True:
        candidate = os.path.join(current_dir, basename)
        if os.path.exists(candidate):
            return candidate
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break
        current_dir = parent_dir
    raise FileNotFoundError(f"File '{basename}' not found in current or parent directories")

def get_dotenv() -> dict[str, str]:
    if not get_dotenv.env_vars:
        try:
            with open(locate_file(".env"), 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or '=' not in line:
                        continue
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    get_dotenv.env_vars[key] = value
        except FileNotFoundError:
            pass
    return get_dotenv.env_vars
get_dotenv.env_vars = {}

# get variable from environment or from .env file
def getenv(varname: str) -> str:
    # first check environment variables
    if varname in os.environ:
        return os.environ[varname]
    # then check .env file
    dotenv = get_dotenv()
    if varname in dotenv:
        return dotenv[varname]
    # finally raise error
    raise LookupError(f"Variable '{varname}' not found in environment or .env file")

def ensure_basedir(filepath):
    basedir = os.path.dirname(filepath)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    # end if

def today():
    return datetime.now().strftime("%Y-%m-%d")
