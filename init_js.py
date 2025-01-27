from pathlib import Path


def next_api(directory_name: str, mission_name: str) -> None:

    with open(f"{directory_name}\\{mission_name}\\editor\\animation\\init.js", 'r') as init:

        for line in init.readlines():
            if "animation" in line:
                print("init.js has ANIMATION!!")
                return

    Path(f"{directory_name}\\{mission_name}\\editor\\animation\\init.js").write_text(
'''requirejs(['ext_editor_io2', 'jquery_190'],
    function (extIO, $) {
        var io = new extIO({});
        io.start();
    }
);''')

    print("\\editor\\animation\\init.js - OK")