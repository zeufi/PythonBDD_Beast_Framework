
import shutil
import subprocess
import argparse
from datetime import datetime
import os
import pathlib
import platform


def add_drivers_to_path():

    print("Adding webdrivers to path.")
    curr_file_path = pathlib.Path(__file__).parent.absolute()

    if platform.system() == 'Darwin':
        webdriver_path = os.path.join(curr_file_path, 'tests/webdrivers', 'mac')
    elif platform.system() == 'Windows':
        webdriver_path = os.path.join(curr_file_path, 'tests/webdrivers', 'wimdows')
    elif platform.system() == 'Linux':
        webdriver_path = os.path.join(curr_file_path, 'tests/webdrivers', 'linux')
    else:
        raise Exception("Unknown platform. Unable to add webdrivers to path.")

    current_path = os.environ.get('PATH')
    new_path = webdriver_path + ':' + current_path
    os.environ['PATH'] = new_path


def get_unique_run_id():

    if os.environ.get("BUILD_NUMBER"):
        unique_run_id = os.environ.get("BUILD_NUMBER")
    elif os.environ.get("CUSTOM_BUILD_NUMBER"):
        unique_run_id = os.environ.get("CUSTOM_BUILD_NUMBER")
    else:
        unique_run_id = datetime.now().strftime('%Y%m%d%H%M%s')

    os.environ['UNIQUE_RUN_ID'] = unique_run_id

    return unique_run_id


def create_output_directory(prefix='results_'):

    global run_id
    if not run_id:
        raise Exception("Variable 'run_id' is not set. Unable to create output directory")

    curr_file_path = pathlib.Path(__file__).parent.absolute()
    dir_to_create = os.path.join(curr_file_path, prefix + str(run_id))
    os.mkdir(dir_to_create)

    print(f"Created output directory: {dir_to_create}")

    return dir_to_create


if __name__ == '__main__':
    run_id = get_unique_run_id()

    parser = argparse.ArgumentParser()
    parser.add_argument('--test_dir', required=True, help="Location of test file.")
    parser.add_argument('--behave_options', type=str, required=False,
                        help="String of behave options. For Example tags like '-t <tag name>'")

    args = parser.parse_args()
    test_dir = args.test_dir
    behave_options = '' if not args.behave_options else args.behave_options

    output_dir = create_output_directory()
    json_out_dir = os.path.join(output_dir, 'json_report_out.json')
    # junit_out_dir = os.path.join(output_dir, 'junit_report_out')

    command = f'behave -k --no-capture -f json.pretty -o "{json_out_dir}" ' \
              f'{behave_options} ' \
              f'{test_dir} ' \
        # f'--junit --junit-directory {junit_out_dir} '

    print(f"Running command: {command}")

    rs = subprocess.run(command, shell=True)

    files = os.path.join(os.getcwd())
    src = json_out_dir
    dst = os.path.join(files, 'tests/report_generation')
    copy_out_dir = os.path.join(shutil.copy2(src, dst))
