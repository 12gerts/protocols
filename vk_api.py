from argparse import ArgumentParser, Namespace
from time import sleep
import os
import requests

TOKEN = os.environ.get('TOKEN')


def arg_parser() -> Namespace:
    parser = ArgumentParser(description="Parser of friends and followers of VK")

    parser.add_argument("--id", "-i",
                        type=int,
                        required=True,
                        help="User id in VK")

    parser.add_argument("--friends", "-fr",
                        help='Display a list of friends',
                        action="store_true")

    parser.add_argument("--followers", "-fo",
                        help='Display a list of followers',
                        action="store_true")

    return parser.parse_args()


def request(method: str, user_id: str) -> dict:
    return requests.get(
        'https://api.vk.com/method/' + method,
        params={
            'access_token': TOKEN,
            'user_id': user_id,
            'v': 5.131,
            'lang': 'ru'
        }
    ).json()['response']


def get_followers(user_id: str) -> None:
    print(f'\nFollowers of {get_user_name(user_id)}')
    try:
        answers = request("users.getFollowers", user_id)['items']
        get_names(answers)
    except KeyError:
        print('Unable to get followers: private profile')


def get_friends(user_id: str) -> None:
    print(f'\nFriends of {get_user_name(user_id)}')
    try:
        answers = request("friends.get", user_id)['items']
        get_names(answers)
    except KeyError:
        print('Unable to get friends: private profile')


def get_user_name(user_id: str) -> str:
    answer = request("users.get", user_id)[0]
    return f'{answer["first_name"]} {answer["last_name"]}'


def get_names(ids: list) -> None:
    if not ids:
        return

    for amount, _id in enumerate(ids):
        if amount % 5 == 0:
            sleep(0.5)
        print(get_user_name(_id))


def main():
    args = arg_parser()

    if args.friends:
        get_friends(args.id)

    if args.followers:
        get_followers(args.id)


if __name__ == "__main__":
    main()
