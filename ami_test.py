import bios
import ami
import term


def save_exit_confirm(item):
    r = ami.message_box(
        "Save Changes and Exit", "Save configuration and reset?", ["Yes", "No"]
    )
    if r == 0:
        term.exit_func()


def discard_exit_confirm(item):
    r = ami.message_box(
        "Discard Changes and Exit",
        "Discard configuration and reset?",
        ["Yes", "No"],
    )
    if r == 0:
        term.exit_func()


def discard_confirm(item):
    r = ami.message_box(
        "Discard Changes", "Discard configuration changes?", ["Yes", "No"]
    )
    if r == 0:
        item["value"] = "OK"


exit_page: bios.Page = {
    "title": "Exit",
    "items": [
        {
            "title": "Save Changes and Exit",
            "type": "option",
            "help": "Save changed settings and reset the computer\nF10 can be used for this",
            "function": save_exit_confirm,
        },
        {
            "title": "Discard Changes and Exit",
            "type": "option",
            "help": "Discard changed settings and reset the computer",
            "function": discard_exit_confirm,
        },
        {
            "title": "Discard Changes",
            "type": "option",
            "help": "Discard changed settings",
            "function": discard_confirm,
        },
        {
            "title": "Restore Defaults",
            "type": "option",
            "help": "Restore all settings to defaults and reset the computer",
        },
    ],
}


def test_dialog(item):
    r = ami.message_box("Title", "Are you sure to perform?", ["Yes", "No"])
    if r == 0:
        item["value"] = "Clear"


hwinfo_page: bios.Page = {
    "title": "Hardware Info",
    "items": [
        {
            "title": "Project Version",
            "value": "1.23.4567",
        },
        {
            "title": "Project Build Date",
            "value": "01/01/1970",
        },
        None,
        {
            "title": "Project Version",
            "value": "1.23.4567",
        },
        {
            "title": "Project Build Date",
            "value": "01/01/1970",
        },
    ],
}


main_page: bios.Page = {
    "title": "Main",
    "items": [
        {
            "title": "Project Version",
            "value": "1.23.4567",
        },
        {
            "title": "Project Build Date",
            "value": "01/01/1970",
        },
        None,
        {
            "title": "System Date",
            "value": "01/01/1970",
            "type": "option",
            "level": 0,
            "help": "Set the current system date",
            "function": test_dialog,
        },
        {
            "title": "System Time",
            "value": "00:00:00",
            "type": "option",
            "level": 0,
            "help": "Set the current system time",
        },
        None,
        {
            "title": "Hardware Information",
            "type": "subpage",
            "level": 0,
            "help": "View details about installed hardware",
            "subpage": bios.new_page_generator(hwinfo_page),
        },
    ],
}


boot_page: bios.Page = {
    "title": "Boot",
    "items": [
        {
            "title": "Boot mode",
            "type": "select",
            "values": [
                "UEFI only",
                "UEFI and CSM",
                "Legacy",
            ],
            "value": 0,
            "help": "Set the UEFI boot mode\n"
            + "UEFI only = Boot only UEFI devices\n"
            + "UEFI and CSM = Boot both UEFI and legacy devices\n"
            + "Legacy = Boot only legacy devices",
        },
        {
            "title": "Network boot",
            "type": "select",
            "values": ["Disabled", "Enabled"],
            "value": 1,
            "help": "Enable/Disable network boot",
        },
        None,
        {
            "title": "Change boot order",
            "type": "option",
            "help": "Edit the order of boot devices",
            "function": test_dialog,
        },
    ],
}

admin_pages: bios.PageGenerators = [
    bios.new_page_generator(main_page),
    bios.new_page_generator(boot_page),
    bios.new_page_generator(exit_page),
]


def main():
    ami.bios_screen(admin_pages)


if __name__ == "__main__":
    main()
