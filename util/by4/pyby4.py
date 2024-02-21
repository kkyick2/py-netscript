import os
import subprocess
import argparse

BY4EXE_PATH = "C:/Users/jackyyick/projects_local/BCompare64_v422/BCompare.exe"
SETTING_PATH = os.path.join(os.path.dirname(__file__), 'by4_setting', 'by4_setting.txt').replace("\\","/")

def process_input_run_by4(arg1_before, arg2_after, arg3_title, arg4_out):
    '''
        run BCompare.exe for folder and files compare
        @param: example
            arg1_before = "C:/Users/jackyyick/output/empf_pr/20240213_0430/prne_conf"
            arg2_after = "C:/Users/jackyyick/output/empf_pr/20240214_0430/prne_conf"
            arg3_title = "diff report
            arg4_out = "diff_report.html"
            by4exe = "C:/Users/jackyyick/projects_local/BCompare64_v422/BCompare.exe"
            setting = "@C:/Users/jackyyick/projects_local/python/py_by4/by4_setting/by4_setting.txt"

            REMARK: bcompare is a window program, the path syntex should be '/' Slash, NOT '\' Backslash
    '''
    print(f'##############################################')
    print(f'### EXE_PATH: {BY4EXE_PATH}')
    print(f'### SETTING : {SETTING_PATH}')
    print(f'### Before: {arg1_before}')
    print(f'### After: {arg2_after}')
    print(f'### Title: {arg3_title}')
    print(f'### html_path: {arg4_out}')

    subprocess.run([BY4EXE_PATH, '@' + SETTING_PATH, arg1_before, arg2_after, arg3_title, arg4_out])
    return


if __name__ == "__main__":
    # example1:
    # C:\Users\jackyyick\projects_local\python\py-by4>
    #          python 1pyrunby4.py C:/Users/jackyyick/output/empf_pr/20240213_0430/prne_conf C:/Users/jackyyick/output/empf_pr/20240214_0430/prne_conf -t "test title" -o "test.html"
    parser = argparse.ArgumentParser()
    parser.add_argument("before_path", help="before path of the folder")
    parser.add_argument("after_path", help="after path of the folder")
    parser.add_argument("-t", "--html_title", help="title of output html", default="diff report")
    parser.add_argument("-o", "--out_path", help="output path of the output html", default="diff_report.html")
    args = parser.parse_args()

    print(args)

    arg1 = args.before_path
    arg2 = args.after_path
    arg3 = args.html_title
    arg4 = args.out_path

    process_input_run_by4(arg1,arg2,arg3,arg4)