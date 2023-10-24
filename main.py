import requests, json, sys, os, importlib.util

url = "http://theblackbox.blackcompanydev.fr/"

# Get student login
def read_login():
    if os.path.exists('setting.json'):
        f = open('setting.json')
        data = json.load(f)
        if data["login"] == "":
            return "Be sure of having setup the setting.json with your login and your login isn't empty!"
        return data['login']
    else:
        return "Be sure of having setup the setting.json with your login !"

# Print describe
def describe():
    output = requests.get(url).json()
    for pair in output:
        print (f"{pair}: \n\t{output[pair]}")

# do the post to test
def test_result(script_name, string, login):
    json_object = {
        "login" : login,
        "string" : string
    }
    output = requests.get(f"{url}{script_name}/string", params=json_object).json()
    for pair in output:
        print (f"{pair}: \n\t[{output[pair]}]")
    return output

# Permit to get student function
def get_function (script_path, script_name):
    spec = importlib.util.spec_from_file_location("module.name", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, script_name)

# Do the test in function of script
def execute_test(script_name, function_getted, login):
    if script_name == "caesar" and sys.argv[2] != "get" and sys.argv[3] != "lore":
        return function_getted(sys.argv[2], int(sys.argv[3]))
    elif script_name == "caesar" and sys.argv[2] == "get" and sys.argv[3] == "lore":
        return function_getted("", "")
    elif script_name == "rsa" and sys.argv[3] == "result":
        return sys.argv[2]
    elif script_name == "rsa" and sys.argv[3] == "getlore":
        return sys.argv[2]
    elif script_name == "xor":
        return function_getted(sys.argv[2], sys.argv[3])
    elif script_name == "djb2" or script_name == "md5" or script_name == "sha0":
        return function_getted(login + sys.argv[2])
    else:
        return "No function found, this case is umprobable, if you read the subject"

# Main Execution of the Software
def main ():
    if (login := read_login()) != "Be sure of having setup the setting.json with your login !" and login != "Be sure of having setup the setting.json with your login and your login isn't empty!":
        if len(sys.argv) < 2:
            describe()
        else:
            script_name, script_path = sys.argv[1], f"./{sys.argv[1]}/{sys.argv[1]}.py"
            if os.path.exists(script_path):
                result_student_function = execute_test(script_name, get_function(script_path, script_name), login)
                res = test_result(script_name, result_student_function, login)
            else:
                print(f"\"{script_path}\" isn't found!\nBe sure to have place your program at root of your repository, and to have created the good architecture, (use tree)")

if __name__ == "__main__":
    main()