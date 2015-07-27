# Techno-Tiki Gradient Code Generator
# Create by Tony DiCola
#
# Generate the code for a gradient of colors that can be used as an animation
# with the techno-tiki project.  See more details from the guide at:
#   https://learn.adafruit.com/techno-tiki-rgb-led-torch/overview
#
# Usage: Run with the --help parameter to see usage information printed.  In
# general the tool should be run with at least two command line arguments, the
# starting and ending hex color values.  For example to generate a gradient from
# red to blue run as follows:
#   python gradient.py ff0000 0000ff
#
# Released under a MIT license: http://opensource.org/licenses/MIT
import argparse


def color_to_rgb(color):
    """Convert hex color code to 8-bit R, G, B values."""
    # Strip out any preceeding pound sign.
    if color is not None:
        color = color.strip('#')
    # Convert to hex then grab component byte values and return them as a tuple.
    try:
        value = int(color, 16)
    except ValueError:
        raise RuntimeError('Expected color value to be in HTML format (like #ff0000) but found: {0}'.format(color))
    return (((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF))

def rgb_to_color(r, g, b):
    """Convert R, G, B values to hex string."""
    r, g, b = int(r) & 0xFF, int(g) & 0xFF, int(b) & 0xFF
    value = r << 16 | g << 8 | b
    return '0x{0:06X}'.format(value)


def lerp(x, x0, x1, y0, y1):
    """Linear interpolation of value y given position x, starting x0, ending x1,
    starting y0 and ending y1.
    """
    x = float(x)
    x0, x1 = float(x0), float(x1)
    y0, y1 = float(y0), float(y1)
    return y0+(y1-y0)*((x-x0)/(x1-x0))


# Build command line parser and parse arguments.
print('Techno-Tiki Gradient Code Generator\n')
parser = argparse.ArgumentParser(description='Techno-Tiki Gradient Code Generator')
parser.add_argument('--steps', '-s', action='store', default=8, type=int,
                    help='Number of animation steps to be generated.')
parser.add_argument('start', action='store',
                    help='Starting color (in HTML format like ff0000).')
parser.add_argument('end', action='store',
                    help='Ending color (in HTML format like 00ff00).')
args = parser.parse_args()

# Get the component RGB colors.
r1, g1, b1 = color_to_rgb(args.start)
r2, g2, b2 = color_to_rgb(args.end)

# Interpolate colors and print result code.
values = map(lambda i: rgb_to_color(int(lerp(i, 0, args.steps-1, r1, r2)),
                                    int(lerp(i, 0, args.steps-1, g1, g2)),
                                    int(lerp(i, 0, args.steps-1, b1, b2))),
             range(args.steps))
print('Copy and paste this code as the gradient animation value:\n')
print('{{ {0} }}\n'.format(', '.join(values)))
