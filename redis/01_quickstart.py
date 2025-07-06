import asyncio

from redis.asyncio import Redis


async def play_with_strings(client: Redis) -> None:
    key = "composite:key"
    # SET composite:key composite:value
    await client.set(key, "composite:value")
    # GET composite:key
    print(await client.get(key))

    # multiple SETting and GETting
    key1, key2 = "skey1", "skey2"
    await client.mset({key1: "skey1_value", key2: "skey2_value"})
    print(await client.mget([key1, key]))

    await client.delete(key, key1, key2)


async def play_with_lists(client: Redis) -> None:
    list_key = "list-key"

    await client.delete(list_key)

    # RPUSH key elem [elem] -> from the right
    await client.rpush(list_key, -1, 3.14)
    print(f"{list_key}[0] = {await client.lindex(list_key, 0)}")

    # LPUSH key elem [elem] -> from the left
    await client.lpush(list_key, "2a")
    print(f"{list_key}[0] = {await client.lindex(list_key, 0)}")

    # [2a, -1, 3.14] -> [2a, 21, 3.14]
    await client.lset(list_key, 1, "21")
    print(f"{list_key}[1] = {await client.lindex(list_key, 1)}")

    # BTW, values are typed "str" -> only formality to please type checkers
    await client.linsert(list_key, where="AFTER", refvalue="21", value="42")
    await client.linsert(
        list_key, where="BEFORE", refvalue="42", value="42"
    )  # duplicate
    await client.linsert(
        list_key, where="AFTER", refvalue="42", value="-1"
    )  # the first occurrence

    print(f"LPOP -> {await client.lpop(list_key, count=1)}")
    print(f"RPOP -> {await client.rpop(list_key, count=1)}")
    print(f"LREM -> {await client.lrem(list_key, count=1, value='-1')}")

    # totals
    print(f"{list_key}: {await client.lrange(list_key, start=0, end=-1)}")
    print(f"{list_key}: {await client.llen(list_key)}")


async def play_with_sets(client: Redis) -> None:
    set1_key = "set1-key"
    await client.delete(set1_key)

    await client.sadd(set1_key, "spam", "ham", "eggs")
    print(f"set1 MEMBERS = {await client.smembers(set1_key)}")
    print(f"set1 CARDINALITY = {await client.scard(set1_key)}")
    print(f"set1 ISMEMBER (ham) = {await client.sismember(set1_key, 'ham')}")

    await client.srem(set1_key, "spam")
    print("the 'spam' element is deleted from the set1")

    print("Introducing the set2")

    set2_key = "set2-key"
    await client.delete(set2_key)

    await client.sadd(set2_key, "spam", "eggs")
    print(f"set2 MEMBERS = {await client.smembers(set2_key)}")

    print(f"set1 UNION set2: {await client.sunion([set1_key, set2_key])}")
    print(f"set1 INTER set2: {await client.sinter([set1_key, set2_key])}")
    print(f"set1 - set2: {await client.sdiff([set1_key, set2_key])}")
    print(f"set2 - set1: {await client.sdiff([set2_key, set1_key])}")


async def play_with_zsets(client: Redis) -> None:
    zset1_key = "zset1-key"
    await client.delete(zset1_key)

    await client.zadd(
        zset1_key,
        {
            "user1": 1,
            "user2": 2,
            "user3": 3,
            "user1": 0,  # noqa: F601
        },
    )
    print(f"ZCARDINALITY: {await client.zcard(zset1_key)}")

    print(f"all users: {await client.zrange(zset1_key, 0, -1)}")
    print(
        f"all users with scores: {await client.zrange(zset1_key, 0, -1, withscores=True)}"
    )

    for user in ("user1", "user2", "user3"):
        print(f"{user} rank: {await client.zrank(zset1_key, user)}")

    # # Увеличение score
    # r.zincrby('leaderboard', 50, 'user1')

    print(f"user1 INCRBY 12: {await client.zincrby(zset1_key, 12, 'user1')}")
    print(f"user1 new score: {await client.zscore(zset1_key, 'user1')}")
    print(f"all users again: {await client.zrange(zset1_key, 0, -1)}")
    print(
        f"all users (ranks reversed): {await client.zrevrange(zset1_key, 0, -1, withscores=True)}"
    )
    print(
        f"some users (by scores): {await client.zrangebyscore(zset1_key, 0, 5, withscores=True)}"
    )
    print(
        f"some users (scores reversed): {await client.zrevrangebyscore(zset1_key, 5, 0, withscores=True)}"
    )


async def play_with_hsets(client: Redis) -> None:
    hset_key = "hset-key"

    await client.delete(hset_key)

    # Creating a hash
    await client.hset(hset_key, "name", "Alice")
    await client.hset(hset_key, "age", "25")  # to please a type checker
    await client.hset(hset_key, "email", "alice@example.com")

    # HSETNX example
    await client.hsetnx(
        hset_key, "name", "Bob"
    )  # This won't change the name as it already exists

    # Retrieving values
    print(f"name = {await client.hget(hset_key, 'name')}")
    print(f"fields = {await client.hmget(hset_key, ['name', 'age'])}")

    # Getting all fields and values
    print(f"all = {await client.hgetall(hset_key)}")

    # Checking existence
    print(f"exists = {await client.hexists(hset_key, 'name')}")

    # Getting keys and values separately
    print(f"keys = {await client.hkeys(hset_key)}")
    print(f"values = {await client.hvals(hset_key)}")

    # Length of hash
    print(f"length = {await client.hlen(hset_key)}")

    # Increment operations
    await client.hincrby(hset_key, "age", 1)  # Increments age by 1
    await client.hincrbyfloat(hset_key, "height", 0.5)  # Increments height by 0.5

    # Deleting fields
    await client.hdel(hset_key, "email")  # Deletes the email field


async def main():
    # decode_responses=True
    # Getting data: from binary to text
    r = Redis(decode_responses=True)

    for name, play in {
        "STRINGs": play_with_strings,
        "LISTs": play_with_lists,
        "SETs": play_with_sets,
        "ZSETs": play_with_zsets,
        "HSETs": play_with_hsets,
    }.items():
        print(f"Play with {name}")
        await play(client=r)
        print()


if __name__ == "__main__":
    asyncio.run(main())
