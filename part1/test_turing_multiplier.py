# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states
transitions = {
    # مرحله 1 و بررسی شرایط خاص
    ('q0', '1'): ('q1', 'X', 'R'),
    ('q1', '0'): ('q_step2_back', '0', 'L'),
    
    # حالت خاص: اگر عدد اول فقط یک '1' بود
    ('q_step2_back', 'X'): ('q_step2_clear0', '', 'R'),
    ('q_step2_clear0', '0'): ('qa', '', 'R'),
    
    # ادامه مرحله 3
    ('q1', '1'): ('q2', 'X', 'R'),
    
    # مرحله 4: حرکت تا رسیدن به '0'
    ('q2', '1'): ('q2', '1', 'R'),
    ('q2', '0'): ('q3', '0', 'R'),
    
    # مرحله 5: تبدیل اولین '1' پس از '0' به 'Y'
    ('q3', '1'): ('q4', 'Y', 'R'),
    
    # مرحله 6 و 7: حرکت به سمت انتهای رشته و قرار دادن '#'
    ('q4', '1'): ('q4', '1', 'R'),
    ('q4', ''): ('q_step8', '#', 'R'),
    
    # اگر قبلاً '#' گذاشته شده بود، از آن عبور کن
    ('q4', '#'): ('q_step11', '#', 'R'),
    
    # مرحله 8: پر کردن اولین خانه خالی با '1' و بازگشت
    ('q_step8', ''): ('q5', '1', 'L'),
    
    # مرحله 9: بازگشت به چپ تا رسیدن به 'Y'
    ('q5', '1'): ('q5', '1', 'L'),
    ('q5', '#'): ('q5', '#', 'L'),
    ('q5', 'Y'): ('q6', 'Y', 'R'),
    
    # مرحله 10: بررسی بعد از 'Y'
    ('q6', '1'): ('q7', 'Y', 'R'),
    
    # مرحله 13: اگر بعد از 'Y' به '#' رسیدیم
    ('q6', '#'): ('q8', '#', 'L'),
    
    # مرحله 11: حرکت به راست تا رسیدن به اولین خانه خالی برای نوشتن '1'
    ('q7', '1'): ('q7', '1', 'R'),
    ('q7', '#'): ('q_step11', '#', 'R'),
    ('q_step11', '1'): ('q_step11', '1', 'R'),
    ('q_step11', ''): ('q5', '1', 'L'),
    
    # مرحله 13 (ادامه): تبدیل 'Y'ها به '1'
    ('q8', 'Y'): ('q8', '1', 'L'),
    
    # مرحله 14 و 15: رسیدن به '0' و بازگشت تا 'X'
    ('q8', '0'): ('q9', '0', 'L'),
    ('q9', '1'): ('q9', '1', 'L'),
    
    # مرحله 16: رسیدن به 'X' و حرکت به راست برای بررسی عدد اول
    ('q9', 'X'): ('q15_check', 'X', 'R'),
    
    # مرحله 17 و 18: بررسی اینکه آیا عدد اول تمام شده است یا خیر
    ('q15_check', '1'): ('q2', 'X', 'R'),
    ('q15_check', '0'): ('q_clean_leftmost', '0', 'L'),
    
    # مرحله 18 (پاکسازی): رفتن به ابتدای نوار و پاک کردن 'X'ها
    ('q_clean_leftmost', 'X'): ('q_clean_leftmost', '', 'L'),
    ('q_clean_leftmost', ''): ('q_clean_rightwards', '', 'R'),
    ('q_clean_rightwards', ''): ('q_clean_rightwards', '', 'R'),
    
    # مرحله 18 (ادامه): پاک کردن '0' میانی
    ('q_clean_rightwards', '0'): ('q_clean_skip1s', '', 'R'),
    ('q_clean_skip1s', '1'): ('q_clean_skip1s', '1', 'R'),
    
    # مرحله 19: تبدیل '#' به '1'
    ('q_clean_skip1s', '#'): ('q_find_blank_end', '1', 'R'),
    
    # مرحله 20 و 21: رفتن به انتهای نوار و پاک کردن آخرین '1' اضافی
    ('q_find_blank_end', '1'): ('q_find_blank_end', '1', 'R'),
    ('q_find_blank_end', ''): ('q_remove_last_1', '', 'L'),
    ('q_remove_last_1', '1'): ('qa', '', 'L')
}


if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:",w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w, step_limit=1000)

        print()

    # SHOULD ACCEPT
    run("110111")
    # outputs 111111

    # SHOULD ACCEPT
    run("11101111")
    # outputs 111111111111

    run("01111")
