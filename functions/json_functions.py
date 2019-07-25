import json


def update_data(user):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except IOError:
        print("Failed to find 'users.json' file. Creating")
        create_file = open("users.json", "w+")
        create_file.write("{}")
        create_file.close()

    users[str(user.id)] = {}
    users[str(user.id)]['chromosomes'] = 0
    users[str(user.id)]['deleteMemes'] = False

    with open("users.json", "w") as f:
        json.dump(users, f)


def update_chromosomes(user, add):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except IOError:
        print("Failed to find 'users.json' file. Creating")
        create_file = open("users.json", "w+")
        create_file.write("{}")
        create_file.close()

    try:
        users[str(user.id)]['chromosomes'] += add
    except KeyError:
        update_data(user)
        update_chromosomes(user, add)
        return

    with open("users.json", "w") as f:
        json.dump(users, f)


def check_chromosomes(user):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except IOError:
        print("Failed to find 'users.json' file. Creating")
        create_file = open("users.json", "w+")
        create_file.write("{}")
        create_file.close()

    try:
        chromosomes = users[str(user.id)]['chromosomes']
    except KeyError:
        update_data(user)
        chromosomes = check_chromosomes(user)

    return chromosomes


def transfer_chromosomes(user, to_user, amount):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except IOError:
        print("Failed to find 'users.json' file. Creating")
        create_file = open("users.json", "w+")
        create_file.write("{}")
        create_file.close()

    try:
        users[str(user.id)]['chromosomes'] -= amount
    except KeyError:
        update_data(user)
        transfer_chromosomes(user, to_user, amount)
        return

    try:
        users[str(to_user.id)]['chromosomes'] += amount
    except KeyError:
        update_data(to_user)
        transfer_chromosomes(user, to_user, amount)
        return

    with open("users.json", "w") as f:
        json.dump(users, f)


def check_moderation(user):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except IOError:
        print("Failed to find 'users.json' file. Creating")
        create_file = open("users.json", "w+")
        create_file.write("{}")
        create_file.close()

    try:
        return users[str(user.id)]['deleteMemes']
    except KeyError:
        users[str(user.id)]['deleteMemes'] = False
        with open("users.json", "w") as f:
            json.dump(users, f)
        return False

'''
def change_moderation(user, modname):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except IOError:
        print("Failed to find 'users.json' file. Creating")
        create_file = open("users.json", "w+")
        create_file.write("{}")
        create_file.close()

    try:
        if users[str(user.id)][modname]:
            users[str(user.id)][modname] = False
        else:
            users[str(user.id)][modname] = True
    except KeyError:
        users[str(user.id)][modname] = True
        with open("users.json", "w") as f:
            json.dump(users, f)
'''