def next_api(directory_name, mission_name):

    init = open(f"{directory_name}\\{mission_name}\\editor\\animation\\init.js", 'r')
    for line in init.readlines():
        if "animation" in line:
            print("init.js has ANIMATION!!")
            break

    try:
        file = open(f"{directory_name}\\{mission_name}\\editor\\animation\\init.js", 'w')
        file.write(
'''requirejs(['ext_editor_io2', 'jquery_190'],
    function (extIO, $) {
        var io = new extIO({});
        io.start();
    }
);
''')
    except:
        print("init.js - PROBLEM!!")
    else:
        print("\\editor\\animation\\init.js - OK")
    finally:
        file.close()