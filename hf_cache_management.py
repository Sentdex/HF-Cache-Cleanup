import os
import shutil

import colorama
import inquirer
from colorama import Fore, Style
from huggingface_hub.constants import HF_HUB_CACHE

colorama.init()


def get_size_in_gb(size_in_bytes):
    return round(size_in_bytes / (1024 * 1024 * 1024), 2)


def get_color_by_size(size_in_gb):
    if size_in_gb >= 5.0:  # 5 GB or more
        return Fore.RED
    elif size_in_gb >= 1.0:  # 1 GB to 4.99 GB
        return Fore.YELLOW
    else:  # Less than 1 GB
        return Fore.GREEN


def main(cache_dir: str = HF_HUB_CACHE):
    cached_hf_repos = os.listdir(cache_dir)

    models_list = []
    for item in cached_hf_repos:
        item_path = os.path.join(cache_dir, item)
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path)
        elif os.path.isdir(item_path):
            size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, _, filenames in os.walk(item_path) for filename in filenames)
        size_gb = get_size_in_gb(size)
        color = get_color_by_size(size_gb)
        models_list.append((color + f"{item} - {size_gb} GB" + Style.RESET_ALL, item))

    models_list = [model for model in models_list if model[1] not in (".locks", "version.txt")]
    # Sort so datasets and models are grouped separately
    models_list = sorted(models_list, key=lambda x: x[1])

    if not models_list:
        print(Fore.GREEN + "No models found in cache - exiting!" + Style.RESET_ALL)
        exit()

    questions = [
        inquirer.Checkbox(
            'models_to_delete',
            message="Select models to delete. Navigate with up/down arrows, use right/left arrows select/deselect, enter to continue",
            choices=models_list,
        ),
        inquirer.Text('confirm', message="Are you sure you want to delete those models? Type 'yes' to confirm"),
    ]

    answers = inquirer.prompt(questions)

    if answers['confirm'].lower() == 'yes':
        total_space_freed = 0
        for model in answers['models_to_delete']:
            model_path = os.path.join(cache_dir, model)
            if os.path.exists(model_path):
                if os.path.isdir(model_path):
                    size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, _, filenames in os.walk(model_path) for filename in filenames)
                    shutil.rmtree(model_path)
                else:
                    size = os.path.getsize(model_path)
                    os.remove(model_path)
                size_gb = get_size_in_gb(size)
                total_space_freed += size_gb
                print(Fore.GREEN + f"Removed {model} from cache. Freed {size_gb} GB." + Style.RESET_ALL)
            else:
                print(Fore.RED + f"{model} not found in cache." + Style.RESET_ALL)

        if total_space_freed > 0:
            print(Fore.CYAN + f"\nTotal space freed: {round(total_space_freed, 2)} GB." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "\nNo space was freed." + Style.RESET_ALL)

    total, used, free = shutil.disk_usage(cache_dir)
    print(Fore.MAGENTA + f"\nAvailable disk space after cleanup: {get_size_in_gb(free)} GB" + Style.RESET_ALL)


if __name__ == '__main__':
    from fire import Fire
    Fire(main)
