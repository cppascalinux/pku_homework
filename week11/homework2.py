import random, asyncio

x = 0

async def produce():
    global x 
    x += 1
    await asyncio.sleep(1)
    print("Produce %d" % x)
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

asyncio.run(consumer(3))