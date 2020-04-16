import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# =================================
# KAFKA SETTINGS
# =================================
KAFKA_SERVER = "{}:{}".format(os.environ.get("KAFKA_IP", "192.168.1.175"),
                              os.environ.get("KAFKA_PORT", "9092"))
KAFKA_CLIENT_ID = 'opennebula-kafka-publisher'
KAFKA_API_VERSION = (1, 1, 0)
KAFKA_OPENNEBULA_TOPIC = os.environ.get("KAFKA_OPENNEBULA_TOPIC", "nfvi.tid-onlife.opennebula")
KAFKA_TRAFFIC_MANAGER_TOPIC = os.environ.get("KAFKA_TRAFFIC_MANAGER_TOPIC", "trafficmanager.uc2.metrics")

# =================================
# OSM SETTINGS
# =================================
OSM_IP = os.environ.get("OSM_IP", "192.168.83.27")
OSM_ADMIN_CREDENTIALS = {"username": os.environ.get("OSM_USER", "admin"),
                         "password": os.environ.get("OSM_PWD", "password")}
OSM_COMPONENTS = {"UI": 'http://{}:80'.format(OSM_IP),
                  "NBI-API": 'https://{}:9999'.format(OSM_IP),
                  "RO-API": 'http://{}:9090'.format(OSM_IP)}

# =================================
# XML-RPC SERVER SETTINGS
# =================================
XML_RPC_SERVER = "http://{}/RPC2".format(os.environ.get("XML_RPC_SERVER", '192.168.83.20:2633'))
XML_RPC_SESSION = os.environ.get("XML_RPC_SESSION", "username:password")

# =================================
# STANDALONE VM IDS (traffic manager etc)
# =================================
NO_OSM_VM_IDS = os.environ.get("NO_OSM_VM_IDS", "677")

# =================================
# METRICS SETTINGS
# =================================
METRICS_LIST = [
    {"name": "memory", "type": "gauge", "unit": "kbytes"},
    {"name": "vcpu", "type": "gauge", "unit": "vcpu"},
    {"name": "nettx", "type": "gauge", "unit": "bytes"},
    {"name": "netrx", "type": "gauge", "unit": "bytes"},
    {"name": "diskrdbytes", "type": "gauge", "unit": "bytes"},
    {"name": "diskwrbytes", "type": "gauge", "unit": "bytes"},
    {"name": "diskwriops", "type": "gauge", "unit": "iops"},
    {"name": "diskrdiops", "type": "gauge", "unit": "iops"},
    {"name": "disk_size", "type": "gauge", "unit": "mbytes"}
]
# =================================
# SCHEDULER SETTINGS
# =================================
SCHEDULER_MINUTES = os.environ.get("SCHEDULER_MINUTES", 1)  # minutes
KAFKA_TRAFFIC_SCHEDULER_SECONDS = 5

# ==================================
# LOGGING SETTINGS
# ==================================
# See more: https://docs.python.org/3.5/library/logging.config.html
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': "[%(asctime)s] - [%(name)s:%(lineno)s] - [%(levelname)s] %(message)s",
        },
        'simple': {
            'class': 'logging.Formatter',
            'format': '%(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
        },
        'one_worker': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "{}/logs/one_worker.log".format(PROJECT_ROOT),
            'mode': 'w',
            'formatter': 'detailed',
            'level': 'DEBUG',
            'maxBytes': 2048 * 2048,
            'backupCount': 4,
        },
        'traffic_manager_worker': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "{}/logs/traffic_manager_worker.log".format(PROJECT_ROOT),
            'mode': 'w',
            'formatter': 'detailed',
            'level': 'DEBUG',
            'maxBytes': 1024 * 1024,
            'backupCount': 4,
        },
        'errors': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "{}/logs/error.log".format(PROJECT_ROOT),
            'mode': 'w',
            'level': 'ERROR',
            'formatter': 'detailed',
            'maxBytes': 2024 * 2024,
            'backupCount': 5,
        },
    },
    'loggers': {
        'traffic_manager_worker': {
            'level': 'DEBUG',
            'handlers': ['traffic_manager_worker']
        },
        'one_worker': {
            'level': 'DEBUG',
            'handlers': ['one_worker']
        },
        'errors': {
            'handlers': ['errors']
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
}
