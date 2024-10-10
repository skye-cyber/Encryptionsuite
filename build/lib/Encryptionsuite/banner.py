from .colors import (DYELLOW, DBLUE, BBYELLOW, BBCYAN, RESET)


def _banner_():
    banner = F'''{DBLUE}
    ffffffffffff     eeeeeeeeeee    DDDDD&&8_
    ffffffffffff     EEEEEEEEEEE    DDD DDD-D8
    fff              EE             DDD      DD
    {DBLUE}fff              EE             DDD       DD   {BBCYAN}   88888     {RESET}
    {DYELLOW}fff              EEEEEEEEEEE    DDD        DD   {BBCYAN}  8888 8888888888888  {RESET}
    {DYELLOW}ffffffffffff     EEEEEEEEEEE    DDD        DD   {BBYELLOW}  8  O  8888888888>  {RESET}
    {DYELLOW}ffffffffffff     EE             DDD        DD   {BBCYAN}  8888 8888888888888{RESET}
    {DBLUE}fff              EE             DDD        DD   {BBCYAN}  88888   {RESET} {DBLUE}
    fff              EE             DDD       DD
    fff              EEEEEEEEEEE    DDDDDDD D D
    fff              EEEEEEEEEEE    DDDDD DD ,
    {RESET}'''

    print(banner)


_banner_()
