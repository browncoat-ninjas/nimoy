import sys
from nimoy.spec_runner import SpecRunner


def main():
    result = SpecRunner().run()
    sys.exit(not result.wasSuccessful())


if __name__ == '__main__':
    main()
