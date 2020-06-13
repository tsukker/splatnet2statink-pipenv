import json
import os
import sys

import iksm
import splatnet2statink

attrs = ["api_key", "cookie", "user_lang", "session_token"]
A_VERSION = splatnet2statink.A_VERSION


# Mainly manages Cookie.
# TODO: can be only used as singleton because of a fixed filepath.
class Config:
    def get_config_path(self):
        if getattr(sys, 'frozen', False):
            app_path = os.path.dirname(sys.executable)
        elif __file__:
            app_path = os.path.dirname(__file__)
        config_path = os.path.join(app_path, "config.txt")
        assert (config_path)
        return config_path

    def write(self):
        config_path = self.get_config_path()
        config_file = open(config_path, "w")
        config_file.seek(0)
        config_file.write(
            json.dumps(self.config_data,
                       indent=4,
                       sort_keys=True,
                       separators=(',', ': ')))
        config_file.close()

    def __init__(self):
        config_path = self.get_config_path()
        if not os.path.exists(config_path):
            print("Generating new config file.")
            self.config_data = {attr: "" for attr in attrs}
            self.write()
        else:
            config_file = open(config_path, "r")
            self.config_data = json.load(config_file)
            config_file.close()
        assert (self.config_data)

    def get(self, attr):
        return self.config_data[attr]

    # See: gen_new_cookie() from splatnet2statink.py
    def update_cookie(self, reason):
        '''Attempts to generate a new cookie in case the provided one is invalid.'''

        manual = False

        if reason == "blank":
            print("Blank cookie.")
        elif reason == "auth":  # authentication error
            print("The stored cookie has expired.")
        else:  # server error or player hasn't battled before
            print(
                "Cannot access SplatNet 2 without having played at least one battle online."
            )
            sys.exit(1)
        if self.config_data["session_token"] == "":
            print(
                "session_token is blank. Please log in to your Nintendo Account to obtain your session_token."
            )
            new_token = iksm.log_in(A_VERSION)
            if new_token == None:
                print(
                    "There was a problem logging you in. Please try again later."
                )
            else:
                if new_token == "skip":  # user has opted to manually enter cookie
                    manual = True
                    print(
                        "\nYou have opted against automatic cookie generation and must manually input your iksm_session cookie.\n"
                    )
                else:
                    print("\nWrote session_token to config.txt.")
                self.config_data["session_token"] = new_token
                self.write()
        elif self.config_data["session_token"] == "skip":
            manual = True
            print(
                "\nYou have opted against automatic cookie generation and must manually input your iksm_session cookie. You may clear this setting by removing \"skip\" from the session_token field in config.txt.\n"
            )

        if manual:
            new_cookie = iksm.enter_cookie()
        else:
            print("Attempting to generate new cookie...")
            acc_name, new_cookie = iksm.get_cookie(self.get("session_token"),
                                                   self.get("user_lang"),
                                                   A_VERSION)
        self.config_data["cookie"] = new_cookie
        self.write()
        if manual:
            print("Wrote iksm_session cookie to config.txt.")
        else:
            print("Wrote iksm_session cookie for {} to config.txt.".format(
                acc_name))
