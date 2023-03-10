import json
import sys
import uuid

valid_expertise_values = ['Getting Started', 'Tutorial', 'Concepts and Functionality', 'Code Optimization', 'Reference Designs and End to End']
#deprecated_toolchain_values = ['dpcpp', 'icc']
valid_toolchain_values = ['cl', 'clang', 'clang++', 'dpcpp', 'dpcpp-cl', 'gcc', 'g++', 'icc', 'icpc', 'icpx', 'icx', 'ifort', 'jupyter']
valid_languages_values = ['cpp', 'fortran', 'python']
valid_target_device_values = ['CPU', 'GPU', 'FPGA']
#deprecated_os_values = ['darwin']
valid_os_values = ['darwin', 'linux', 'windows']
valid_builder_values = ['cli', 'cmake', 'ide', 'make']

def check_guid(data):
    if 'guid' not in data:
        print('guid is a required field in sample.json.')
        sys.exit(4)

    try:
        uuid.UUID(data['guid'])
    except ValueError:
        print('guid is not a valid GUID.')
        sys.exit(4)

def check_name(data):
    if 'name' not in data:
        print('name is a required field in sample.json.')
        sys.exit(5)

    if len(data['name']) > 99:
        print('name cannot exceed 99 characters.')
        sys.exit(5)

def check_description(data):
    if 'description' not in data:
        print('description is a required field in sample.json.')
        sys.exit(6)

    if len(data['description']) > 250:
        print('description cannot exceed 250 characters.')
        sys.exit(6)

def check_expertise(data):
    if 'expertise' not in data:
        print('expertise is a required field in sample.json.')
        sys.exit(7)

    if data['expertise'] not in valid_expertise_values:
        print('expertise must contain only one the following values: ' + ', '.join(valid_expertise_values) + '.')
        sys.exit(7)

def check_toolchain(data):
    if 'toolchain' not in data:
        print('toolchain is a required field in sample.json.')
        sys.exit(8)

    #if set(data['toolchain']).issubset(set(deprecated_toolchain_values)) == True:
    #    print('toolchain: ' + ', '.join(data['toolchain']) + ' is deprecated. Please use at least one of the following values: ' + ', '.join(valid_toolchain_values) + '.')
    #    sys.exit(8)

    if set(data['toolchain']).issubset(set(valid_toolchain_values)) == False:
        print('toolchain must contain at least one of the following values: ' + ', '.join(valid_toolchain_values) + '.')
        sys.exit(8)

def check_languages(data):
    if 'languages' not in data:
        print('languages is a required field in sample.json.')
        sys.exit(9)

    try:
        languages = data['languages']

        for language in languages:
            not_valid = True
            for valid_language in valid_languages_values:
                if valid_language in language:
                    not_valid = False
                    break

            if not_valid:
                print('languages must contain at least one of the following values: ' + ', '.join(valid_languages_values) + '.')
                sys.exit(9)
    except:
        sys.exit(9)

def check_target_device(data):
    if 'targetDevice' not in data:
        print('targetDevice is a required field in sample.json.')
        sys.exit(10)

    if set(data['targetDevice']).issubset(valid_target_device_values) == False:
        print('targetDevice must contain at least one of the following values: ' + ', '.join(valid_target_device_values) + '.')
        sys.exit(10)

def check_os(data):
    if 'os' not in data:
        print('os is a required field in sample.json.')
        sys.exit(11)

    #if set(data['os']).issubset(set(deprecated_os_values)) == True:
    #    print('os: ' + ', '.join(data['os']) + ' is deprecated. Please use one of the following values: ' + ', '.join(valid_os_values) + '.')
    #    sys.exit(10)

    if set(data['os']).issubset(set(valid_os_values)) == False:
        print('os must contain at least one of the following values: ' + ', '.join(valid_os_values) + '.')
        sys.exit(11)

def check_builder(data):
    if 'builder' not in data:
        print('builder is a required field in sample.json.')
        sys.exit(12)

    if set(data['builder']).issubset(valid_builder_values) == False:
        print('builder must contain at least one of the following values: ' + ', '.join(valid_builder_values) + '.')
        sys.exit(12)

def check_ci_tests(data):
    not_valid = False

    if 'ciTests' not in data:
        print('ciTests is a required field in sample.json.')
        sys.exit(13)

    try:
        os_list = data['os']
        ci_os_obj = data['ciTests']

        for os in os_list:
            if os not in ci_os_obj:
                print(os + ' is a missing under the ciTests object.')
                not_valid = True
            else:
                for ciTest in ci_os_obj[os]:
                    if 'steps' not in ciTest:
                        print('steps is a required field under ciTests/' + os + '.')
                        not_valid = True

        if not_valid:
            sys.exit(14)
    except:
        sys.exit(14)

def main(argv):
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' <filename>')
        sys.exit(1)

    try:
        f = open(sys.argv[1])
    except:
        print(sys.argv[1] + ' not found.')
        sys.exit(2)

    try:
        data = json.load(f)
    except:
        print(sys.argv[1] + ' is not a valid json file.')
        sys.exit(3)

    check_guid(data)
    check_name(data)
    check_expertise(data)
    check_toolchain(data)
    check_languages(data)
    check_target_device(data)
    check_os(data)
    check_builder(data)
    check_ci_tests(data)

    print(sys.argv[1] + ' is a valid sample.json file.')
    sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])
