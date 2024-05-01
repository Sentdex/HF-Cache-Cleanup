  GNU nano 4.8                                                    model_management.py                                                              
import os
import shutil
from transformers import TRANSFORMERS_CACHE
import colorama
from colorama import Fore, Style

colorama.init()

def get_size_in_mb(size_in_bytes):
    return round(size_in_bytes / (1024 * 1024), 2)

def get_color_by_size(size_in_mb):
    if size_in_mb >= 5120:  # 5 GB or more
        return Fore.RED
    elif size_in_mb >= 1024:  # 1 GB to 4.99 GB
        return Fore.YELLOW
    else:  # Less than 1 GB
        return Fore.GREEN

cache_dir = TRANSFORMERS_CACHE
downloaded_models_and_tokenizers = os.listdir(cache_dir)

print(Fore.CYAN + "Downloaded Models and Tokenizers:" + Style.RESET_ALL)
for item in downloaded_models_and_tokenizers:
    item_path = os.path.join(cache_dir, item)
    if os.path.isfile(item_path):
        size = os.path.getsize(item_path)
        size_mb = get_size_in_mb(size)
        color = get_color_by_size(size_mb)
        print(color + f"{item} - {size_mb} MB" + Style.RESET_ALL)
    elif os.path.isdir(item_path):
        size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, _, filenames in os.walk(item_path) for filename in filenames)
        size_mb = get_size_in_mb(size)
        color = get_color_by_size(size_mb)
        print(color + f"{item} - {size_mb} MB" + Style.RESET_ALL)

total, used, free = shutil.disk_usage(cache_dir)
print(Fore.MAGENTA + f"\nAvailable disk space: {get_size_in_mb(free)} MB" + Style.RESET_ALL)

print(Fore.BLUE + "\n" + 20 * '-' + Style.RESET_ALL)
model_to_remove = input(Fore.RED + "model_name to remove: " + Style.RESET_ALL)
model_path = os.path.join(cache_dir, model_to_remove)

if os.path.exists(model_path):
    if os.path.isdir(model_path):
        shutil.rmtree(model_path)
    else:
        os.remove(model_path)
    print(Fore.GREEN + f"Removed {model_to_remove} from cache." + Style.RESET_ALL)
else:
    print(Fore.RED + f"{model_to_remove} not found in cache." + Style.RESET_ALL)
