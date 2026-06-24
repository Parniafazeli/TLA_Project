# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

# ماشین تورینگ برای جمع دو عدد یکانی
transitions = {
    # مرحله 1: رد شدن از 1های عدد اول و یافتن جداکننده 0
    ('q0', '1'): ('q0', '1', 'R'),
    ('q0', '0'): ('q1', '1', 'R'),   # تبدیل 0 به 1 و رفتن به مرحله بعد

    # مرحله 2: عبور از عدد دوم تا رسیدن به انتهای نوار
    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', ''): ('q2', '', 'L'),     # رسیدیم به blank -> یک قدم به چپ

    # مرحله 3: پاک کردن آخرین 1 (اضافی) و پذیرش
    ('q2', '1'): ('qa', '', 'L'),    # آخرین 1 را پاک کرده و به حالت پذیرش می‌رویم
}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:", w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w)
        print()

    # تست‌های مورد نیاز
    run("110111")      # 2+3 = 11111
    run("11101111")    # 3+4 = 1111111
    run("0111")        # 0+3 = 111