import os
CONFIG_COEAI_API_KEY = "coeai-_9d5O7c-ei761wsqowkhmBNxPeaP-wIP"

def _env_bool(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, str(default)))
    except Exception:
        return default


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, str(default)))
    except Exception:
        return default


APP_HOST = os.environ.get("SAHARA_HOST", "0.0.0.0")
APP_PORT = _env_int("SAHARA_PORT", 8501)

DB_PATH = os.environ.get("SAHARA_DB_PATH", "sahara.db")
TOKEN_SECRET = os.environ.get("SAHARA_TOKEN_SECRET", "change-this-secret-in-prod")
TOKEN_TTL_SECONDS = _env_int("SAHARA_TOKEN_TTL_SECONDS", 60 * 60 * 24)
OTP_TTL_SECONDS = _env_int("SAHARA_OTP_TTL_SECONDS", 600)
SHOW_DEV_OTP_HINT = _env_bool("SAHARA_DEV_OTP_HINT", False)

COEAI_API_KEY = os.environ.get("COEAI_API_KEY", CONFIG_COEAI_API_KEY)
COEAI_MODEL = os.environ.get("COEAI_MODEL", "deepseek-r1:70b")
COEAI_TIMEOUT_SEC = _env_int("COEAI_TIMEOUT_SEC", 120)
COEAI_HEALTH_TIMEOUT_SEC = _env_int("COEAI_HEALTH_TIMEOUT_SEC", 10)
UPESNET_CONNECTED_FLAG = _env_bool("UPESNET_CONNECTED", False)

DATA_GOV_PROVIDER = os.environ.get("DATA_GOV_PROVIDER", "auto").strip().lower()
DATA_GOV_API_KEY = os.environ.get("DATA_GOV_API_KEY", "")
DATA_GOV_RAPIDAPI_KEY = os.environ.get("DATA_GOV_RAPIDAPI_KEY", "8ffb0d760cmsh6e173047db5d88bp1af498jsn2943f0a9da56")
DATA_GOV_BASE_URL = os.environ.get("DATA_GOV_BASE_URL", "https://api.data.gov.in")
DATA_GOV_RAPIDAPI_BASE_URL = os.environ.get("DATA_GOV_RAPIDAPI_BASE_URL", "https://data-gov-in.p.rapidapi.com")
DATA_GOV_RAPIDAPI_HOST = os.environ.get("DATA_GOV_RAPIDAPI_HOST", "data-gov-in.p.rapidapi.com")
DATA_GOV_TIMEOUT_SEC = _env_float("DATA_GOV_TIMEOUT_SEC", 8.0)
OPENAI_TTS_VOICE = os.environ.get("OPENAI_TTS_VOICE", "alloy")
OPENAI_TTS_MODEL = os.environ.get("OPENAI_TTS_MODEL", "tts-1")

OLLAMA_CONNECT_TIMEOUT_SEC = _env_float("OLLAMA_CONNECT_TIMEOUT_SEC", 5.0)
OLLAMA_READ_TIMEOUT_SEC = _env_float("OLLAMA_READ_TIMEOUT_SEC", 90.0)

HF_HUB_DISABLE_SYMLINKS_WARNING = os.environ.get("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
TOKENIZERS_PARALLELISM = os.environ.get("TOKENIZERS_PARALLELISM", "false")
TRANSFORMERS_VERBOSITY = os.environ.get("TRANSFORMERS_VERBOSITY", "error")
