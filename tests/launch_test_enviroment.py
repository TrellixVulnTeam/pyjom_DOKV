import time
import os


def launchProgramWithTerminal(
    directory, intepreter, executable, sleep=None, no_terminal=False
):
    try:
        if type(sleep) in [int, float]:
            if sleep > 0:  # logic shortcut please?
                time.sleep(sleep)
            else:
                raise Exception("negative or zero sleep duration:", sleep)
        directory = os.path.abspath(directory)
        assert os.path.exists(directory)
        os.chdir(directory)
        executable_path = os.path.join(directory, executable)
        assert os.path.exists(executable_path)
        command = f'{"gnome-terminal -- " if not no_terminal else ""}{intepreter} {executable_path}'
        return command
    except:
        import traceback

        traceback.print_exc()
        print("failed while launching program with parameters:")
        print(
            f"[D]:{directory}\n[I]{intepreter}\n[E]{executable}\n[C]{dict(sleep=sleep, no_terminal=no_terminal)}"
        )
        breakpoint()
    return None


def executeCommand(command):
    print("executing command:", command)
    os.system(command)


# common paths
pyjom_directory = "/root/Desktop/works/pyjom"
pyjom_tests = os.path.join(pyjom_directory, "tests")
pyjom_externals = os.path.join(pyjom_directory, "externals")

# interpreters
node_exec = "node"
python3_exec = "python3"
bash_exec = "bash"

launchList = [
    # launch billibili recommendation server
    [
        [
            os.path.join(pyjom_tests, "bilibili_video_recommendation_server"),
            python3_exec,
            "test.py",
        ],
        {},
    ],
    # launch qq cqhttp
    [[os.path.join(pyjom_tests, "qq_go_cqhttp"), bash_exec, "launch.sh"], {}],
    # make sure milvus is running.
    [
        [
            os.path.join(pyjom_tests, "video_phash_deduplication"),
            bash_exec,
            "config_milvus.sh",
        ],
        dict(no_terminal=True),
    ],
    # launch netease api server. we need it to download new music, currently.
    # video phash is the last step among all filters.
    [
        [os.path.join(pyjom_externals, "NeteaseCloudMusicApi"), bash_exec, "launch.sh"],
        {},
    ],  # port is 4042. port 4000 is used. don't know why.
    # how to check avaliability of netease cloud music api?
    [
        [os.path.join(pyjom_tests, "karaoke_effects"), bash_exec, "load_translator.sh"],
        {},
    ],
    [
        [
            os.path.join(pyjom_tests, "redis_music_info_persistance"),
            bash_exec,
            "launch_redis.sh",
        ],
        dict(sleep=1),
    ],
    [
        [os.path.join(pyjom_tests, "random_giphy_gifs"), node_exec, "nodejs_server.js"],
        dict(sleep=1),
    ],
    [
        [
            os.path.join(pyjom_tests, "nsfw_violence_drug_detection"),
            node_exec,
            "nsfwjs_test.js",
        ],
        dict(sleep=1),
    ],
]

for argumentList, kwargs in launchList:
    try:
        assert type(kwargs) == dict
        [directory, intepreter, executable] = argumentList
        command = launchProgramWithTerminal(directory, intepreter, executable, **kwargs)
        if command is not None:
            raise Exception("command is None")
        else:
            executeCommand(command)
    except:
        import traceback

        traceback.print_exc()
        print("error when decomposing program launch parameters")
        print(f"[AL]{argumentList}\n[KW]{kwargs}")
        breakpoint()
