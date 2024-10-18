class print_c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    MESSAGE = '\033[94m'
    INFO = '\033[96m'
    
    @staticmethod
    def success(message):
        print(f"{print_c.SUCCESS}[SUCCESS] {message}{print_c.ENDC}")
    
    @staticmethod
    def error(message):
        print(f"{print_c.ERROR}[ERROR] {message}{print_c.ENDC}")
        
    @staticmethod
    def warning(message):
        print(f"{print_c.WARNING}[WARNING] {message}{print_c.ENDC}")
        
    @staticmethod
    def message(message):
        print(f"{print_c.MESSAGE}[MESSAGE] {message}{print_c.ENDC}")
        
    @staticmethod
    def info(message):
        print(f"{print_c.INFO}[INFO] {message}{print_c.ENDC}")