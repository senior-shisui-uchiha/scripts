#!usr/bin/env python

import asyncio


async def async_worker(number, divider, future):
    print('Worker {} started'.format(number))
    await asyncio.sleep(0)
    print(number / divider)
    future.set_result(number / divider)
    return number / divider


async def wait_for_future(future):
    result = await future
    print('Future result: {}'.format(result))
    return result


async def gather_worker():
    fut = [asyncio.Future(),
           asyncio.Future(),
           asyncio.Future(),
           asyncio.Future(),
           asyncio.Future()]
    result = await asyncio.gather(
        async_worker(50, 10, fut[0]),
        wait_for_future(fut[0]),
        async_worker(60, 10, fut[1]),
        wait_for_future(fut[1]),
        async_worker(70, 10, fut[2]),
        wait_for_future(fut[2]),
        async_worker(80, 10, fut[3]),
        wait_for_future(fut[3]),
        async_worker(90, 10, fut[4]),
        wait_for_future(fut[4]),
    )
    print(result)


event_loop = asyncio.get_event_loop()
task_list = [gather_worker()]
tasks = asyncio.wait(task_list)
event_loop.run_until_complete(tasks)
event_loop.close()
