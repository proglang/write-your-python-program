import time
import threading
# do not import writeYourProgram unqualified. Otherwise, module importing the drawingLib through
# `import drawingLib as *` use the check function imported from drawingLib and then the
# magic for reporting the number of tests failed and succeeded no longer works.
import writeYourProgram as _w

Size = _w.Record('Size', 'width', float, 'height', float)
Point = _w.Record('Point', 'x', float, 'y', float)
ShapeKind = _w.Enum('ellipsis', 'rectangle')
Color = _w.Enum('red', 'green', 'blue', 'yellow', 'black', 'white')
FixedShape = _w.Record('FixedShape',
    'shape', ShapeKind,
    'color', Color,
    'size', Size,
    'position', Point
)

from tkinter import Tk, Canvas, Frame, BOTH

# coordinate system: origin is in the upper left corner
def _transformPoint(p, windowSize: Size):
    return (p[0] * 100 + windowSize.width/2, p[1] * -100 + windowSize.height/2)

def _renderFixedShape(prim: FixedShape, windowSize: Size, canvas):
    sz = prim.size
    pos = prim.position
    coords = [
        (pos.x - sz.width/2, pos.y - sz.height/2),
        (pos.x + sz.width/2, pos.y - sz.height/2),
        (pos.x + sz.width/2, pos.y + sz.height/2),
        (pos.x - sz.width/2, pos.y + sz.height/2)
    ]
    coords = [_transformPoint(p, windowSize) for p in coords]
    color = prim.color
    if prim.shape == 'rectangle':
        canvas.create_polygon(coords, fill=color, outline=color)
    elif prim.shape == 'ellipsis':
        upperLeft = coords[0]
        lowerRight = coords[2]
        canvas.create_oval(
            upperLeft[0], upperLeft[1],
            lowerRight[0], lowerRight[1],
            fill=color,
            outline=color
        )

def _drawCoordinateSystem(canvas, windowSize: Size):
    x = windowSize.width / 2
    y = windowSize.height / 2
    canvas.create_line(x, 0, x, windowSize.height, dash=(4,2))
    canvas.create_line(0, y, windowSize.width, y, dash=(4,2))

class _WyppFrame(Frame):
    def __init__(self, diags, windowSize, withCoordinateSystem):
        super().__init__()
        self.master.title("Write Your Python Program")
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)
        if withCoordinateSystem:
            _drawCoordinateSystem(canvas, windowSize)
        for d in diags:
            _renderFixedShape(d, windowSize, canvas)
        canvas.pack(fill=BOTH, expand=1)

def drawFixedShapes(
    shapes: _w.Sequence[FixedShape],
    withCoordinateSystem=False,
    stopAfter=None) -> None:
    root = Tk()
    winWidth = 800
    winHeight = 800
    ex = _WyppFrame(shapes, Size(winWidth, winHeight), withCoordinateSystem)
    root.geometry(f"{winWidth}x{winHeight}+50+50")
    root.lift()
    # bring window to front
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)
    if stopAfter:
        def close():
            time.sleep(stopAfter)
            print('Closing drawing window automatically ...')
            root.destroy()
        t = threading.Thread(target=close, daemon=True)
        t.start()
    root.mainloop()
