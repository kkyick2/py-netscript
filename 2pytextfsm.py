#!/usr/bin/env python
# by kkyick2
# import pkg
import os
import pandas as pd
import ntc_templates
import textfsm
from datetime import datetime

NEXTLINE = '\n'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_CMD_DIR = 'cmdoutput'
OUT_XLS_DIR = 'output'


def _load_template(device_type, command, templates_dir):
    # _load_template function will load correct template
    with open(f"{templates_dir}/{device_type}_{command}.textfsm") as f:
        return textfsm.TextFSM(f)


def _parse_each_file():
    # _parse_each_file will prepare a dataframe containing parsed content of each file.
    df = pd.DataFrame()

    for device_type in sorted(os.listdir(OUT_CMD_DIR)):
        for file in sorted(os.listdir(os.path.join(OUT_CMD_DIR, device_type))):
            print(os.path.join(device_type, file))

            template.Reset()  # otherwise entires from next loop item adds to the previous loop item,
            OUT_CMD_TXT = os.path.join(OUT_CMD_DIR, device_type, file)
            with open(OUT_CMD_TXT) as f:
                text = f.read()

            df_parsed = pd.DataFrame(template.ParseTextToDicts(text))
            df_parsed.insert(0, 'DEVICE_NAME', file[:-19])
            # df = df.append(df_parsed) # append method is deprecated and will be removed from pandas
            df = pd.concat([df, df_parsed])
    return df


def _write_to_excel(df_list):
    # this function will write the dataframes for each command into an excel file.
    DATETIME = datetime.now().strftime("%Y%m%d_%H%M")
    writer = pd.ExcelWriter('output/parsed_commands_' + DATETIME + '.xlsx', engine='xlsxwriter')
    for df, sheetname in df_list:
        df.to_excel(writer, sheet_name=sheetname, index=False)
        workbook = writer.book
        worksheet = writer.sheets[sheetname]
        cell_format = workbook.add_format()
        cell_format.set_text_wrap()
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        # worksheet.set_column('A:E', 20, cell_format)
    writer.save()


if __name__ == "__main__":
    # Find the folder where ntc_templates are installed.
    TEMPLATES_DIR = os.path.dirname(os.path.dirname(ntc_templates.__file__)) + '/ntc_templates/templates'
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    device_type = 'cisco_ios'
    commands = [
        'show_version',
        'show_inventory',
        # 'show_environment_power_all',
        'show_vlan',
        'show_interfaces',
        #'show_interfaces_switchport',
        # 'show_ip_interface',
        'show_ip_interface_brief',
        'show_ip_bgp_summary',
        'show_ip_bgp',
        'show_ip_bgp_neighbors',
        'show_ip_route',
         # 'show_standby_brief',
         # 'show_mac-address-table',
         # 'show_ip_arp',
        'show_cdp_neighbors_detail',
        'show_clock',

    ]
    # Create a seperate df for each command thereby seperate sheet for each command for all devices.
    df_list = []
    for command in commands:
        print(f"Parsing the cmdoutput of {device_type} {command}\n!")
        template = _load_template(device_type, command, TEMPLATES_DIR)
        df_list.append([_parse_each_file(), command])
    _write_to_excel(df_list)