#!/usr/bin/env python3

def callback_handler(is_one: bool = True):
    def clback(callback):
        def printer(msg: str):
            if is_one:
                print("1")
            else:
                print("One")
            callback(msg)
            print("2")
        return printer
    return clback


@callback_handler(is_one=False)
def iamcallback(msg: str):
    print(msg)


def main():
    iamcallback("hello")


if __name__ == '__main__':
    main()
