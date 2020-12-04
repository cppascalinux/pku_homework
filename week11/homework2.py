import random, asyncio

async def produce():
    x = random.randint(20,30)
    await asyncio.sleep(1)
    print("Produce")
    return x
async def consumer(num):
    count = 0
    while True:
        item = await produce()
        await asyncio.sleep(1)
        print("Consume %d" % item)
        count += 1
        if count == num:
            break

asyncio.run(consumer(10)) # available in version >= 3.7