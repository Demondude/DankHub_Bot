import json
import os
import random
import sys


def create_settings():

    TOKEN = input("Write you bot's token: ")
    trapDir = input("Trap folder's full directory: ")
    memeDir = input("Meme folder's full directory: ")
    homeworkDir = input("Homework(NSFW) folder's full directory(TO DISABLE TYPE Disabled): ")
    trashDir = input("Trash directory for deleted files: ")

    with open("config.json", "r") as f:
        config = json.load(f)

    config["token"] = TOKEN
    config["trapGameDir"] = trapDir
    config["memeDir"] = memeDir
    config["homeworkDir"] = homeworkDir
    config["trashDir"] = trashDir

    with open("config.json", "w") as f:
        json.dump(config, f)


def build_dir(initial_dir, database_name):
    image_data = open(database_name, "w+")
    initial_dir_list = os.listdir(initial_dir)
    for image_dir in initial_dir_list:
        if len(os.listdir(initial_dir + os.sep + image_dir)) > 0:
            image_list = os.listdir(initial_dir + os.sep + image_dir)
            for image in image_list:
                if image == "desktop.ini":
                    continue
                image_data.write(initial_dir + os.sep + image_dir + os.sep + image + "\n")
    print("Rebuild Complete.")
    image_data.close()


def scramble_database(file_to_scramble):
    with open(file_to_scramble, 'r') as source:
        data = [(random.random(), line) for line in source]
    data.sort()
    with open(file_to_scramble, 'w') as target:
        for _, line in data:
            target.write(line)


def rebuild_database(dir_file, initialD):
    try:
        os.remove(dir_file)
    except IOError:
        print("Failed to find " + dir_file + " file. Creating")

    build_dir(initialD, dir_file)
    scramble_database(dir_file)


def get_image(dir_file, initialD):

    try:
        if os.stat(dir_file).st_size <= 2:
            print("REBUILDING DATABASE")
            rebuild_database(dir_file, initialD)
    except IOError:
        print("REBUILDING DATABASE")
        rebuild_database(dir_file, initialD)

    image_data = open(dir_file, "r")
    file_choice = image_data.readline().strip("\n")
    image_data.close()

    # TODO implement line remover in python
    if os.name == 'nt':
        os.system("more +1 " + dir_file + ">" + dir_file + "_out")
        os.system("del " + dir_file)
        os.system("move " + dir_file + "_out " + dir_file)
    else:
        os.system('tail -n +2 "' + dir_file + '" > "' + dir_file + '.tmp" && mv "' + dir_file + '.tmp" "' + dir_file + '"')

    

    start = len(initialD) + 1
    end = len(file_choice) - len(os.path.basename(file_choice)) - 1

    # end = (len(file_choice) - len(os.path.basename(file_choice))) - 1
    
    file_owner = file_choice[start:end]
    return file_choice, file_owner


def add_line(report_dir, database_name):
    try:
        image_data = open(database_name, "a")
    except IOError:
        print("File " + database_name + " not found. Creating!")
        image_data = open(database_name, "w+")
    image_data.write(report_dir + "\n")
    image_data.close()


def get_config():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except IOError:
        print("No config found! Creating a new one.")
        create_file = open("config.json", "w+")
        create_file.write("{}")
        create_file.close()
        create_settings()
        print("Done. Restart the bot.")
        sys.exit()

    TOKEN = config["token"]
    trapDir = config["trapGameDir"]
    memeDir = config["memeDir"]
    homeworkDir = config["homeworkDir"]
    trashDir = config["trashDir"]

    return TOKEN, trapDir, memeDir, homeworkDir, trashDir
