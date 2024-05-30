from datetime import datetime, timedelta
import os
from util.by4.pyby4 import process_input_run_by4


def main(conf_dir, env_tag, before_dir, after_dir, odir1_tag, time_tag):
    today = datetime.now().strftime('%Y%m%d')
    input_dir = conf_dir
    report_dir = os.path.join(conf_dir, "diff")
    arg1 = os.path.join(input_dir, env_tag, before_dir, odir1_tag) #yesterday
    arg2 = os.path.join(input_dir, env_tag, after_dir, odir1_tag) #today
    arg3 = odir1_tag + "_diff"
    arg4 = os.path.join(report_dir, odir1_tag + "_" + today + "_diff.html")
    '''
    print(f'##############################################')
    print(f'### Before: {arg1}')
    print(f'### After: {arg2}')
    print(f'### Title: {arg3}')
    print(f'### html_path: {arg4}')
    '''
    process_input_run_by4(arg1, arg2, arg3, arg4)

    return


if __name__ == "__main__":
    conf_dir = r'C:\Users\jackyyick\output'

    before = "before"
    after = "after"

    #####################################
    env_tag = "empf_np"
    odir1_tag = "npne_all"
    time_tag = "_0430"
    main(conf_dir, env_tag, before, after, odir1_tag, time_tag)
    #####################################
    env_tag = "empf_np"
    odir1_tag = "npne_hw"
    time_tag = "_0430"
    main(conf_dir, env_tag, before, after, odir1_tag, time_tag)
    #####################################
    env_tag = "empf_np"
    odir1_tag = "npne_conf"
    time_tag = "_0430"
    main(conf_dir, env_tag, before, after, odir1_tag, time_tag)