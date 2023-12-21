import connect
from bson import ObjectId
from models import Author, Quote
import redis
from redis_lru import RedisLRU


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def name_finder(fullname):
    author = Author.objects(fullname=fullname).first()
    if author:
        quotes = Quote.objects(author=author.id)
        return quotes
    else:
        return 'No quotes for this great man'


@cache
def tag_finder(tag):
    quotes = Quote.objects(tags=tag)
    if quotes:
        return quotes
    else:
        return 'No quotes found'


def tags_finder(tags_list):
    quotes = Quote.objects(tags__in=tags_list)
    if quotes:
        return quotes
    else:
        return 'No quotes found'


def main():
    while True:
        user_input = input('Enter command: ')
        command_list = user_input.split(':')
        result = None
        match command_list[0]:
            case 'exit':
                print('Exit')
                break
            case 'name':
                result = name_finder(command_list[1].lstrip())
            case 'tag':
                result = tag_finder(command_list[1])
            case 'tags':
                values = command_list[1].split(',')
                result = tags_finder(values)
            case _:
                result = 'Invalid command, try again'
        if result:
            if isinstance(result, list):
                for quote in result:
                    print(quote.encode('utf-8').decode('cp1252'))
            elif isinstance(result, Quote):
                print(result.encode('utf-8').decode('cp1252'))
            else:
                print(result)


if __name__ == '__main__':
    main()
