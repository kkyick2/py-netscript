import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR2 = os.path.dirname(os.path.realpath(__file__))
print('root_dir1:    ',ROOT_DIR)
print('root_dir2:    ',ROOT_DIR2)
# print(os.listdir(ROOT_DIR))

print('basename:    ', os.path.basename(__file__))
print('dirname:     ', os.path.dirname(__file__))
print('abspath:     ', os.path.abspath(__file__))
print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))
print('up 1 level:  ', os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))

SETTING = os.path.join(os.path.abspath(__file__), 'by4_setting', 'by4_setting.txt')

print(SETTING)