from demo_games.freddy.enums import EnumCamera


def _getc(x, y):
    return "*" if x == y else " "


def print_map(current_cam: EnumCamera):
    return (

        "               +======+                            \n" +
        "               |CAM1A{}|______                      \n".format(_getc(EnumCamera.CAM1A, current_cam)) +
        "               +======+      |                     \n" +
        "                |            |                     \n" +
        "   +----+_+--+======+--------+--------+            \n" +
        "   |    |_|  |CAM1B{}|                 |            \n".format(_getc(EnumCamera.CAM1B, current_cam)) +
        "+=====+ | |  +======+                 |_+---|      \n" +
        "|CAM5{}| | |                           |_| +=====+  \n".format(_getc(EnumCamera.CAM5, current_cam)) +
        "+=====+ | |                           | | |CAM7{}|_ \n".format(_getc(EnumCamera.CAM7, current_cam)) +
        "   +----+ |                           | | +=====+ |\n" +
        "         +======+                     | |   |-|___|\n" +
        "    +----|CAM1C{}|                     | |   |_____ \n".format(_getc(EnumCamera.CAM1C, current_cam)) +
        "    |    +======+                     | |   |-|   |\n" +
        "    +-----|___________________________| +---+ +---+\n" +
        "                | |         | |    | |             \n" +
        "              +-----+     +-----+ +---------+      \n" +
        "              |     |     |     | |     +=====+    \n" +
        "        +---+ |     |     |     | |     |CAM6{}|    \n".format(_getc(EnumCamera.CAM6, current_cam)) +
        "    +=====+ |_|======+    |+=======+____+=====+    \n" +
        "    |CAM3{}| |_|CAM2A{}|    ||CAM4A{} |               \n".format(_getc(EnumCamera.CAM3, current_cam), _getc(EnumCamera.CAMs2A, current_cam), _getc(EnumCamera.CAMs4A, current_cam)) +
        "    +=====+ | +======+___+|+=======+               \n" +
        "        +---+ +======+   ||+=======+               \n" +
        "              |CAM2B{}|you|_|CAM4B{} |               \n".format(_getc(EnumCamera.CAMs2B, current_cam), _getc(EnumCamera.CAMs4B, current_cam)) +
        "              +======+ {} ||+=======+               \n".format(_getc(EnumCamera.OfficeView, current_cam)) +
        "              +_____||___||_____|                  "
    )
