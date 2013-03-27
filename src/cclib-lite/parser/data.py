# This file is part of cclib (http://cclib.sf.net), a library for parsing
# and interpreting the results of computational chemistry packages.
#
# Copyright (C) 2007, the cclib development team
#
# The library is free software, distributed under the terms of
# the GNU Lesser General Public version 2.1 or later. You should have
# received a copy of the license along with cclib. You can also access
# the full license online at http://www.gnu.org/copyleft/lgpl.html.

__revision__ = "$Revision: 992 $"

import multiarray


class ccData(object):
    """Class for objects containing data from cclib parsers and methods.

    Description of cclib attributes:
        aonames -- atomic orbital names (list)
        aooverlaps -- atomic orbital overlap matrix (array[2])
        atombasis -- indices of atomic orbitals on each atom (list of lists)
        atomcharges -- atomic partial charges (dict of arrays[1])
        atomcoords -- atom coordinates (array[3], angstroms)
        atommasses -- atom masses (array[1], daltons)
        atomnos -- atomic numbers (array[1])
        atomspins -- atomic spin densities (dict of arrays[1])
        charge -- net charge of the system (integer)
        ccenergies -- molecular energies with Coupled-Cluster corrections (array[2], eV)
        coreelectrons -- number of core electrons in atom pseudopotentials (array[1])
        etenergies -- energies of electronic transitions (array[1], 1/cm)
        etoscs -- oscillator strengths of electronic transitions (array[1])
        etrotats -- rotatory strengths of electronic transitions (array[1], ??)
        etsecs -- singly-excited configurations for electronic transitions (list of lists)
        etsyms -- symmetries of electronic transitions (list)
        fonames -- fragment orbital names (list)
        fooverlaps -- fragment orbital overlap matrix (array[2])
        fragnames -- names of fragments (list)
        frags -- indices of atoms in a fragment (list of lists)
        gbasis -- coefficients and exponents of Gaussian basis functions (PyQuante format)
        geotargets -- targets for convergence of geometry optimization (array[1])
        geovalues -- current values for convergence of geometry optmization (array[1])
        grads -- current values of forces (gradients) in geometry optimization (array[3])
        hessian -- elements of the force constant matrix (array[1])
        homos -- molecular orbital indices of HOMO(s) (array[1])
        mocoeffs -- molecular orbital coefficients (list of arrays[2])
        moenergies -- molecular orbital energies (list of arrays[1], eV)
        mosyms -- orbital symmetries (list of lists)
        mpenergies -- molecular electronic energies with Moller-Plesset corrections (array[2], eV)
        mult -- multiplicity of the system (integer)
        natom -- number of atoms (integer)
        nbasis -- number of basis functions (integer)
        nmo -- number of molecular orbitals (integer)
        nocoeffs -- natural orbital coefficients (array[2])
        scfenergies -- molecular electronic energies after SCF (Hartree-Fock, DFT) (array[1], eV)
        scftargets -- targets for convergence of the SCF (array[2])
        scfvalues -- current values for convergence of the SCF (list of arrays[2])
        vibanharms -- vibrational anharmonicity constants (array[2], 1/cm)
        vibdisps -- cartesian displacement vectors (array[3], delta angstrom)
        vibfreqs -- vibrational frequencies (array[1], 1/cm)
        vibirs -- IR intensities (array[1], km/mol)
        vibramans -- Raman intensities (array[1], A^4/Da)
        vibsyms -- symmetries of vibrations (list)
        scannames -- Names of varaibles scanned (list)
        scanenergies -- energies of potential energy surface (list)
        scanparm -- values of parameters in potential energy surface (list of tuples)
        scancoords -- Geometries of each scan step (array[3], angstroms)
        enthaply -- Sum of electronic and thermal Enthalpie (float hartree/particle)
        freeenergy -- Sum of electronic and thermal Free Energies (float hartree/particle)
        temperature -- Tempature used for Thermochemistry (float kelvin)
        entropy -- Entropy (float hartree/particle)
        optdone -- Stores if an optimisation job has completed (boolean)
    (1) The term 'array' refers to a multiarray array
    (2) The number of dimensions of an array is given in square brackets
    (3) Python indexes arrays/lists starting at zero, so if homos==[10], then
            the 11th molecular orbital is the HOMO
    """

    def __init__(self, attributes=None):
        """Initialize the cclibData object.
        
        Normally called in the parse() method of a Logfile subclass.
        
        Inputs:
            attributes - dictionary of attributes to load
        """

        # The expected types for all supported attributes in dectionary,
        # and their names which can be extracted as the keys.
        self._attrtypes = { "aonames":        list,
                            "aooverlaps":     multiarray.arraytype,
                            "atombasis":      list,
                            "atomcharges":    dict,
                            "atomcoords":     multiarray.arraytype,
                            "atommasses":     multiarray.arraytype,
                            "atomnos":        multiarray.arraytype,
                            "atomspins":      dict,
                            "ccenergies":     multiarray.arraytype,
                            "charge":         int,
                            "coreelectrons":  multiarray.arraytype,
                            "etenergies":     multiarray.arraytype,
                            "etoscs":         multiarray.arraytype,
                            "etrotats":       multiarray.arraytype,
                            "etsecs":         list,
                            "etsyms":         list,
                            "fonames":        list,
                            "fooverlaps":     multiarray.arraytype,
                            "fragnames":      list,
                            "frags":          list,
                            'gbasis':         list,
                            "geotargets":     multiarray.arraytype,
                            "geovalues":      multiarray.arraytype,
                            "grads":          multiarray.arraytype,
                            "hessian":        multiarray.arraytype,
                            "homos":          multiarray.arraytype,
                            "mocoeffs":       list,
                            "moenergies":     list,
                            "mosyms":         list,
                            "mpenergies":     multiarray.arraytype,
                            "mult":           int,
                            "natom":          int,
                            "nbasis":         int,
                            "nmo":            int,
                            "nocoeffs":       multiarray.arraytype,
                            "scfenergies":    multiarray.arraytype,
                            "scftargets":     multiarray.arraytype,
                            "scfvalues":      list,
                            "vibanharms":     multiarray.arraytype,
                            "vibdisps":       multiarray.arraytype,
                            "vibfreqs":       multiarray.arraytype,
                            "vibirs":         multiarray.arraytype,
                            "vibramans":      multiarray.arraytype,
                            "vibsyms":        list,
                            "scannames":      list,
                            "scanenergies":   list,
                            "scanparm":       list,
                            "scancoords":     multiarray.arraytype,
                            "enthaply":       float,
                            "freeenergy":     float,
                            "temperature":    float,
                            "entropy":        float,
                            "optdone":        bool
                          }
        # Names of all supported attributes.
        self._attrlist = self._attrtypes.keys()

        # Names of all supported attributes.
        self._attrlist = ['aonames', 'aooverlaps', 'atombasis',
                          'atomcharges', 'atomcoords', 'atommasses', 'atomnos', 'atomspins',
                          'ccenergies', 'charge', 'coreelectrons',
                          'etenergies', 'etoscs', 'etrotats', 'etsecs', 'etsyms',
                          'fonames', 'fooverlaps', 'fragnames', 'frags',
                          'gbasis', 'geotargets', 'geovalues', 'grads',
                          'hessian', 'homos',
                          'mocoeffs', 'moenergies', 'mosyms', 'mpenergies', 'mult',
                          'natom', 'nbasis', 'nmo', 'nocoeffs',
                          'scfenergies', 'scftargets', 'scfvalues',
                          'vibanharms', 'vibdisps', 'vibfreqs', 'vibirs',
                          'vibramans', 'vibsyms', 'scannames', 'scanenergies', 'scanparm',
                          'scancoords', 'enthaply', 'freeenergy', 'temperature', 'entropy', 
                          'optdone']

        # Arrays are double precision by default, but these will be integer arrays.
        self._intarrays = ['atomnos', 'coreelectrons', 'homos']

        # Attributes that should be lists of arrays (double precision).
        self._listsofarrays = ['mocoeffs', 'moenergies', 'scfvalues']
        
        # Attributes that should be dictionaries of arrays (double precision).
        self._dictsofarrays = ["atomcharges", "atomspins"]

        if attributes:
            self.setattributes(attributes)
        
    def listify(self):
        """Converts all attributes that are arrays or lists/dicts of arrays to lists."""
        
        attrlist = [k for k in self._attrlist if hasattr(self, k)]
        for k in attrlist:
            v = self._attrtypes[k]
            if v == multiarray.arraytype:
                setattr(self, k, getattr(self, k).tolist())
            elif v == list and k in self._listsofarrays:
                setattr(self, k, [x.tolist() for x in getattr(self, k)])
            elif v == dict and k in self._dictsofarrays:
                items = getattr(self, k).iteritems()
                pairs = [(key, val.tolist()) for key, val in items]
                setattr(self, k, dict(pairs))
    
    def arrayify(self):
        """Converts appropriate attributes to arrays or lists/dicts of arrays."""
        
        attrlist = [k for k in self._attrlist if hasattr(self, k)]
        for k in attrlist:
            v = self._attrtypes[k]
            precision = 'd'
            if k in self._intarrays:
                precision = 'i'
            if v == multiarray.arraytype:
                setattr(self, k, multiarray.array(getattr(self, k), precision))
            elif v == list and k in self._listsofarrays:
                setattr(self, k, [multiarray.array(x, precision) for x in getattr(self, k)])
            elif v == dict and k in self._dictsofarrays:
                items = getattr(self, k).iteritems()
                pairs = [(key, multiarray.array(val, precision)) for key, val in items]
                setattr(self, k, dict(pairs))

    def getattributes(self, tolists=False):
        """Returns a dictionary of existing data attributes.
        
        Inputs:
            tolists - flag to convert attributes to lists where applicable
        """
    
        if tolists:
            self.listify()
        attributes = {}
        for attr in self._attrlist:
            if hasattr(self, attr):
                attributes[attr] = getattr(self, attr)
        if tolists:
            self.arrayify()
        return attributes

    def setattributes(self, attributes):
        """Sets data attributes given in a dictionary.
        
        Inputs:
            attributes - dictionary of attributes to set
        Outputs:
            invalid - list of attributes names that were not set, which
                      means they are not specified in self._attrlist
        """
    
        if type(attributes) is not dict:
            raise TypeError, "attributes must be in a dictionary"
    
        valid = [a for a in attributes if a in self._attrlist]
        invalid = [a for a in attributes if a not in self._attrlist]
    
        for attr in valid:
            setattr(self, attr, attributes[attr])
        self.arrayify()
        return invalid