# fbUCI, an UCI chess frontend for the Linux framebuffer

![screenshot](https://github.com/mdoege/fbUCI/raw/master/fbuci.png "fbUCI screenshot")

The default engine is ``/usr/bin/stockfish``, but other UCI engine binaries can also be used.

## Prerequisites

Needs [python-chess](https://github.com/niklasf/python-chess) and [Pillow](https://github.com/python-pillow/Pillow)

Framebuffer screen size is set to 1920x1080, so on Raspbian be sure to disable overscan in ``/boot/config.txt``.

You may need to add yourself to the ``video`` group on some Linux distros for permission to use the framebuffer.

## Usage

Enter moves in UCI notation, e.g. ``e2e4``, ``e1g1`` (castling kingside), or ``a7a8q`` (pawn promotion to Queen).

You will play as White by default; to play as Black just add ``black`` as a commandline parameter.

Hit enter to redraw the board; enter ``r`` to rotate board; enter ``q`` to quit.

## License

GPL

Board and piece images are from [Lichess](https://github.com/ornicar/lila).

