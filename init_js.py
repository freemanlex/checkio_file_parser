def next_api(directory_name, mission_name):

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
        return "init.js - PROBLEM!!"
    else:
        return "\\editor\\animation\\init.js - OK"
    finally:
        file.close()