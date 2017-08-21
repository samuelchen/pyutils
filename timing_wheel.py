#!/usr/bin/env python
# coding: utf-8

"""
Timing wheel is a arithmetic for much more timers.

ref: https://blog.acolyer.org/2015/11/23/hashed-and-hierarchical-timing-wheels/

"""

import abc
from collections import OrderedDict
from datetime import datetime, time
import threading
from time import sleep


class IRemind(metaclass=abc.ABCMeta):
    """
    The interface to describe a remind-able class.
    Will be used by ITimingWheel.
    """
    @abc.abstractmethod
    def remind(self):
        raise NotImplementedError


class ITimingWheel(metaclass=abc.ABCMeta):
    # __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def push(self, when, reminder):
        """
        Push a reminder into a wheel slot(when)
        :param when:
        :param reminder:
        :return: index of the reminder
        """
        raise NotImplementedError

    @abc.abstractmethod
    def pop(self, when, reminder):
        """
        pop out a reminder from a wheel slot(when)
        :param when:
        :param reminder: reminder or index
        :return: the reminder
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remind(self, reminder):
        """
        Method to trigger a reminder.
        Implement it yourself for your final logic
        :param reminder: the reminder contains datetime information and context
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def tick(self):
        """
        Make wheel walking one slot. Trigger all reminders in current slot.
        will tick once per second
        """
        raise NotImplementedError

    __lock = threading.Lock()
    worker_thread = None
    started = False

    def worker(self):
        while self.started:
            self.tick()
            sleep(1)

    def start(self):
        """
        Start to roll the timing wheel
        :return:
        """
        assert self.started is False and self.worker_thread is None

        self.worker_thread = threading.Thread(target=self.worker)
        with self.__lock:
            self.started = True
        self.worker_thread.start()

    def stop(self):
        """
        Stop rolling timing wheel
        :return:
        """
        if not self.started:
            return

        assert self.worker_thread is not None

        with self.__lock:
            self.started = False
        self.worker_thread.join(2)

        if self.worker_thread.is_alive():
            self.worker_thread._stop()

        self.worker_thread = None


class TimingWheel(ITimingWheel):
    """
    The implementation of daily timing-wheel timer
    """
    seconds_per_hour = 60 * 60
    seconds_per_minute = 60

    def __init__(self, interval=5*60, init_slots=False, advance_if_not_match_interval=True):
        """
        ctor
        :param interval: tick interval in seconds
        :param init_slots: whether initialize slots when creating.
        :param advance_if_not_match_interval: remind in advance if the time not match interval.
                    (e.g. interval=5, reminder=13:12:32, if true, will remind on 13:12:30.
                     Otherwise, remind on 13:12:35)
        :return:
        """
        assert 0 < interval == int(interval)

        self._interval = interval
        self._total = 24*60*60
        self._slots_count = self._total / self._interval
        self._adv_not_match = advance_if_not_match_interval
        self._wheel = OrderedDict()
        if init_slots:
            self.__init_slots()

        self._cur = None

    def __init_slots(self):
        t = 0

        while t < self._total:
            slot = self.__seconds_to_slot(t)
            self._wheel[slot] = []
            t += self._interval

    def __seconds_to_slot(self, seconds):
        t = seconds
        h = divmod(t, self.seconds_per_hour)[0]
        seconds_for_hours = h * self.seconds_per_hour
        m = divmod(t - seconds_for_hours, self.seconds_per_minute)[0]
        s = t - seconds_for_hours - m * self.seconds_per_minute
        if h > 23:
            h = divmod(h, 24)[1]
        slot = '%02d:%02d:%02d' % (h, m, s)
        return slot

    def interval(self):
        """
        tick interval in seconds
        :return:
        """
        return self._interval

    def _when2slot(self, when):
        assert isinstance(when, datetime) or isinstance(when, time)
        s = when.hour * self.seconds_per_hour + when.minute * self.seconds_per_minute + when.second
        dm = divmod(s, self._interval)
        if dm[1] != 0:
            if self._adv_not_match:
                s -= dm[1]
            else:
                s = s - dm[1] + self._interval
        slot = self.__seconds_to_slot(s)
        return slot

    def pop(self, when, reminder):
        slot = self._when2slot(when)
        if slot in self._wheel:
            self._wheel[slot].remove(reminder)

    def push(self, when, reminder):
        slot = self._when2slot(when)
        if slot not in self._wheel:
            self._wheel[slot] = []
        self._wheel[slot].append(reminder)

    def remind(self, reminder):
        print('remind:', reminder)
        raise NotImplementedError

    def tick(self):
        when = datetime.now()
        slot = self._when2slot(when)
        if slot in self._wheel:
            for reminder in self._wheel[slot]:
                if isinstance(reminder, IRemind):
                    reminder.remind()       # TODO: try/except ?
                else:
                    self.remind(reminder)
                self._wheel[slot].remove(reminder)


class HierarchicalTimingWheel(object):
    pass


if __name__ == '__main__':
    timer = TimingWheel()
    # timer = TimingWheel(advance_if_not_match_interval=False)
    # timer = TimingWheel(init_slots=True, advance_if_not_match_interval=False)
    timer.push(datetime.strptime('15:12:33', '%H:%M:%S'), 'nihao')
    timer.push(datetime.strptime('15:13:33', '%H:%M:%S'), 'hello')
    for k, v in timer._wheel.items():
        print(k, v)

    timer.start()