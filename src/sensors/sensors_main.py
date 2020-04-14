import time
from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

from src.sensors.sensors_entrepot import sonde, sonde1, sonde2, sonde5, sondeWarehouse
from src.sensors.sensors_stores import sondeStore
from src.sensors.utils import end


def launch_sensors(isTest=False, checker=None, fakeClient=None):
    if isTest:
        sonde1(isTest)
        sonde2(isTest)
    else:
        # sondeStore(first=True)
        scheduleYourSensors(BlockingScheduler())  # If you need actualized data :)


def addSchedule(scheduler, sonde, timeToRun=datetime.now(), second=8):
    scheduler.add_job(sonde, 'interval', seconds=second, next_run_time=timeToRun)


def scheduleYourSensors(scheduler):  # pragma: no cover
    print(f"(+) Tipboard  sensors initialisation", flush=True)
    now = datetime.now()
    every = 60 * 30
    # every = 1 * 30
    # scheduler.add_job(sonde1, 'interval', seconds=60*1)
    # addSchedule(scheduler, sondeStore(first=True), timeToRun=now + timedelta(milliseconds=10 * 1), second=1000*60*60*24)

    addSchedule(scheduler, sonde, timeToRun=now + timedelta(milliseconds=1000 * 1), second=every)
    addSchedule(scheduler, sonde5, timeToRun=now + timedelta(milliseconds=1000 * 2), second=60 * 3)
    addSchedule(scheduler, sondeStore, timeToRun=now + timedelta(milliseconds=1000 * 120), second=every)
    addSchedule(scheduler, sondeWarehouse, timeToRun=now + timedelta(milliseconds=1000 * 10), second=every)

    # addSchedule(scheduler, sonde3, timeToRun=now + timedelta(milliseconds=100 * 3), second=every)
    # addSchedule(scheduler, sonde4, timeToRun=now + timedelta(milliseconds=100 * 4), second=every)
    print(f"(+) Tipboard starting schedul task", flush=True)
    scheduler.start()
    return True


def stopTheSensors(localScheduler):
    if localScheduler is not None:
        localScheduler.shutdown()


if __name__ == "__main__":  # pragma: no cover
    print(f"(+) Tipboard  sensors initialisation", flush=True)
    start_time = time.time()
    launch_sensors()
    scheduleYourSensors(BlockingScheduler())  # If you need actualized data :)
    end(title="startUp", start_time=start_time)
