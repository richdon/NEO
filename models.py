# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 17:24:04 2021.

@author: richa
"""
from helpers import cd_to_datetime, datetime_to_str
import copy

"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = info['designation']

        if len(info['name']) == 0:
            self.name = None
        else:
            self.name = info['name']

        if info['diameter'] == '' or info['diameter'] is None:
            self.diameter = float('nan')
        else:
            self.diameter = float(info['diameter'])

        if info['hazardous'] == 'Y':
            self.hazardous = True
        else:
            self.hazardous = False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return (f"{self.designation} ({self.name})")

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous:
            return (f"{self.fullname} has a diameter of {self.diameter:.3f} km"
                    " and is potentially hazardous.")
        else:
            return (f"{self.fullname} has a diameter of {self.diameter:.3f} km"
                    " and is not potentially hazardous.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        """Return a dictionary mapping the NearEarthObjects attribute name to

        its value, and formatting the output to the
        desired format of the JSON.
        """
        serialized = copy.deepcopy(vars(self))

        if serialized.get('name') is None:
            serialized['name'] = str('')

        if 'approaches' in serialized:
            del serialized['approaches']

        serialized['potentially_hazardous'] = serialized.pop('hazardous')
        serialized['diameter_km'] = serialized.pop('diameter')

        return serialized


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = info['des']
        self.time = cd_to_datetime(info['time'])
        self.distance = float(info['distance'])
        self.velocity = float(info['velocity'])

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    def serialize(self):
        """Returns a dictionary mapping the CloseApproach object's attribute name 
        to its value and formatting the output to the desired format of the JSON
        """
        # Create a copy of the reference object to not change the object's values
        serialized = copy.deepcopy(vars(self))

        if 'neo' in serialized:
            del serialized['neo']

        serialized['time'] = datetime_to_str(serialized.get('time'))
        serialized['velocity_km_s'] = serialized.pop('velocity')
        serialized['distance_au'] = serialized.pop('distance')
        serialized['datetime_utc'] = serialized.pop('time')

        return serialized

    
    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return the the attributes of the referenced object with the print statement"""
        
        if self.neo:
            return f" At {self.time_str}, {self.neo.fullname} has a diameter of {self.neo.diameter} approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."
        else:
            return f" AtAt {self.time_str}, {self._designation} approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."
    
    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")