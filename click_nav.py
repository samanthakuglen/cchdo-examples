import json
import click

'''
The purpose of this script is to perform a patch to cchdo with an infile that
is a nav_file in .txt format containing LATITUDE and LONGITUDE information
to update the coordinate information for a cruise with no track
'''
@click.command()
@click.argument('infile', type = click.File('r'), nargs = 1)
@click.argument('outfile', type = click.File('w'), nargs = 1)
def nav(infile, outfile):
    points = []
    for line in infile:
        point = [float(p) for p in line.split()[:2]]
        if point not in points:
            points.append(point)

    linestring = {
    "type": "LineString",
    "coordinates": points
    }

    patch = [
        {"path":"/geometry/track", "op":"replace", "value":linestring}
        ]

    json.dump(patch, outfile)


if __name__ == '__main__':
    nav()
