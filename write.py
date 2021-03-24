"""
Created on Fri Feb 12 00:47:54 2021.

@author: Richard Donald
"""
import csv
import json
import copy
"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output
    row corresponds to the information in a single close approach from the
    `results` stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
    saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation',
                  'name', 'diameter_km', 'potentially_hazardous')

    approaches = copy.deepcopy(results)

    for ca in approaches:
        if ca.neo.name is None:
            ca.neo.name = str('nan')
        if ca.neo.diameter == float('nan'):
            ca.neo.diameter = str('nan')
        if ca.neo.hazardous == 'Y' or ca.neo.hazardous:
            ca.neo.hazardous = str('True')
        elif ca.neo.hazardous == 'N' or ca.neo.hazardous is False:
            ca.neo.hazardous = str('False')

    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for ca in results:
            writer.writerow([ca.time_str, ca.distance, ca.velocity,
                            ca._designation, ca.neo.name, ca.neo.diameter,
                            ca.neo.hazardous])


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is
    a list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to
     where the data should be saved.
    """
    serialized_neos = []

    for app in results:
        if app.neo:
            serial_neo = app.neo.serialize()
            serialized_neos.append(serial_neo)

    serialized_apps = []

    for app in results:
        serial = app.serialize()
        serialized_apps.append(serial)

    for app in serialized_apps:
        for neo in serialized_neos:
            if neo['designation'] == app['_designation']:
                app['neo'] = neo
        del app['_designation']

    serialized_apps[0].get('datetime_utc')

    with open(filename, 'w') as f:
        json.dump(serialized_apps, f, indent=2)
