#!/usr/bin/env python3

# fbUCI, an UCI chess frontend for the Linux framebuffer

import chess, chess.engine
from PIL import Image
import os, sys

# Open an UCI chess engine
if "ntc" in sys.argv:
        engine = chess.engine.SimpleEngine.popen_uci("../nimTUROCHAMP/ntc")
        limit = chess.engine.Limit()
else:
        engine = chess.engine.SimpleEngine.popen_uci("/usr/bin/stockfish")
        limit = chess.engine.Limit(time = 1)    # calculate for one second

# Settings that can be changed here
fbw, fbh = 1920, 1080   # framebuffer dimensions
xoff, yoff = 800, 100   # screen offset
hicolor = (100, 0, 100, 100)       # highlight color (RGBA)

# Do not change these
w, h = 100, 100         # tile dimensions
rotate = False          # Black plays from bottom?

# Open the framebuffer device
f = open("/dev/fb0", "wb")
os.system("clear")

def swap_redblue(im):
        "Swap red and blue channels in image"
        r, g, b, a = im.split()
        return Image.merge("RGBA", (b, g, r, a))

# PIL is RGBA and the framebuffer is BGRA, so swap channels for board image
ib = Image.open("img/maple.png").convert("RGBA")
ib = swap_redblue(ib)

def getpos(x, y):
        "Board coordinates to screen coordinates"
        if rotate:
                return (700 - 100 * x, 100 * y)
        else:
                return (100 * x, 700 - 100 * y)

def blit(im, pos):
        "Copy image im to position pos"
        f.seek(4 * ((pos[1] + yoff) * fbw + pos[0] + xoff))

        iby = im.tobytes()
        for i in range(h):
                f.write(iby[4*i*w:4*(i+1)*w])
                f.seek(4 * (fbw - w), 1)

def put(fn, pos, highlight = False):
        "Display piece image with file name fn at position pos with offset xoff/yoff"
        if fn:
                im = Image.open(fn).convert("RGBA")
                if highlight:
                        ib_crop = Image.new('RGBA', (w, h), hicolor)
                else:
                        ib_crop = ib.crop((pos[0], pos[1], pos[0] + w, pos[1] + h))
                im = Image.alpha_composite(ib_crop, im)
        else:
                if highlight:
                        im = Image.new('RGBA', (w, h), hicolor)
                else:
                        im = ib.crop((pos[0], pos[1], pos[0] + w, pos[1] + h))

        blit(im, pos)

def draw_square(b, i, highlight = False):
        "Draw a square on the board"
        x = chess.square_file(i)
        y = chess.square_rank(i)
        p = b.piece_at(8 * y + x)
        if p:
                if p.color: col = "w"
                else: col = "b"
                fn = "img/" + col + p.symbol().upper() + ".png"
                put(fn, getpos(x, y), highlight = highlight)
        else:
                put("", getpos(x, y), highlight = highlight)

def draw_board(b):
        "Draw complete chessboard on screen"
        for i in range(64):
                draw_square(b, i)

def draw_labels():
        "Draw board labels"
        for x in range(8):
                im = Image.open("img/%s.png" % chr(97 + x)).convert("RGBA")

                pos = getpos(x, -1)
                blit(im, pos)

                pos = getpos(x, 8)
                blit(im, pos)

        for y in range(8):
                im = Image.open("img/%s.png" % chr(49 + y)).convert("RGBA")

                pos = getpos(-1, y)
                blit(im, pos)

                pos = getpos(8, y)
                blit(im, pos)

b = chess.Board()
oldmove = ()
result = None

if "black" in sys.argv:
        player = False
        rotate = True
else: player = True

draw_board(b)
draw_labels()

while b.result() == "*":
        if b.turn == player:
                while True:
                        move = input("Your move? ")
                        if move.strip() == "":
                                draw_board(b)
                                draw_labels()
                                continue
                        if move.strip() == "r":
                                rotate = not rotate
                                draw_board(b)
                                draw_labels()
                                continue
                        if move.strip() == "s" and result:
                                print("Score:", result.info.get("score", "unknown"))
                                continue
                        if move.strip() in ("q", "quit", "exit", "resign"):
                                print("Goodbye!")
                                f.close()
                                engine.quit()
                                sys.exit()
                        try:
                                b.push_uci(move)
                                mm = b.pop()
                        except: print("Sorry?")
                        else: break
        else:
                result = engine.play(b, limit)
                mm = result.move
        if b.turn:
                if player:
                        print("%3u. %-6s  " % (b.fullmove_number, b.san(mm)), end = "", flush = True)
                else:
                        print("%3u. %-6s  " % (b.fullmove_number, b.san(mm)), flush = True)
        else:
                if player:
                        print(b.san(mm), flush = True)
                else:
                        print("... %-6s" % b.san(mm), flush = True)
        b2 = b.copy()
        b.push(mm)
        newmove = []
        for i in range(64):
                if i in oldmove:
                        draw_square(b, i)
                if b.piece_at(i) != b2.piece_at(i):
                        draw_square(b, i, highlight = True)
                        newmove.append(i)
        oldmove = newmove

print
print(b.result())

f.close()
engine.quit()


