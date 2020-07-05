"""
Unit tests for the module.

Thomas Ogden <t@ogden.eu>

"""

import os

import unittest

import numpy as np

from maxwellbloch import mb_solve, t_funcs, spectral, utility

# Absolute path of tests/json directory, so that tests can be called from
# different directories.
JSON_DIR = os.path.abspath(os.path.join(__file__, '../', 'json'))

class TestInit(unittest.TestCase):

    def test_init_default(self):
        """  Test Default Initialise """

        mb_solve_00 = mb_solve.MBSolve()

        self.assertEqual(mb_solve_00.atom.num_states, 1)

        # TODO: And the rest!

    def test_init_00(self):

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mb_solve_01 = mb_solve.MBSolve().from_json(json_path)

@unittest.skip("TODO")
class TestSolveOverThermalDetunings(unittest.TestCase):

    def test_00(self):

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mb_solve_00 = mb_solve.MBSolve().from_json(json_path)

        result_Delta = mb_solve_00.solve_over_thermal_detunings()

        self.assertEqual(len(result_Delta),
                         len(mb_solve_00.thermal_delta_list))

class TestMBSolve(unittest.TestCase):

    def test_mb_solve(self):
        """ Basic test of mb_solve method. """

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mb_solve_00 = mb_solve.MBSolve().from_json(json_path)

        mb_solve_00.mbsolve()

    def test_no_atoms(self):
        """ Setting the number density ampl to 0.0, i.e. no atoms. The end
            pulse should be the same as the start. """

        json_path = os.path.join(JSON_DIR, "mb_solve_no_atoms.json")

        mbs = mb_solve.MBSolve().from_json(json_path)

        mbs.mbsolve(step='euler')

        self.assertEqual(mbs.Omegas_zt.shape, (1, 5, 101))

        # Check that the field at the end of the medium matches the field
        # at the start of the medium.
        self.assertTrue(np.allclose(mbs.Omegas_zt[:, 0, :],
                                    mbs.Omegas_zt[:, -1, :], rtol=1.0e-6))

    def test_no_atoms_ab(self):
        """ Setting the number density to 0.0, i.e. no atoms, with AB step. """

        json_path = os.path.join(JSON_DIR, "mb_solve_no_atoms.json")

        mbs = mb_solve.MBSolve().from_json(json_path)

        mbs.mbsolve(step='ab')

        # Check that the field at the end of the medium matches the field
        # at the start of the medium.
        self.assertTrue(np.allclose(mbs.Omegas_zt[:, 0, :],
                                    mbs.Omegas_zt[:, -1, :], rtol=1.0e-6))

    def test_no_decays(self):
        """ Empty decay list. """

        json_path = os.path.join(JSON_DIR, "mb_solve_no_decays.json")

        mb_solve_nd = mb_solve.MBSolve().from_json(json_path)

        mb_solve_nd.mbsolve()

    def test_no_rabi_freq_t_func(self):
        """ Empty decay list. TODO: No mbsolve, should be in init"""

        json_path = os.path.join(JSON_DIR, "mb_solve_no_rabi_freq_t_func.json")
        mbs = mb_solve.MBSolve().from_json(json_path)

        # self.assertEqual(mbs.ob_atom.fields[0].rabi_freq_t_func,
            # t_funcs.square_1)
        self.assertDictEqual(mbs.atom.fields[0].rabi_freq_t_args,
                             {"ampl_0": 1.0, "on_0": 0.0, "off_0": 1.0})

    def test_two_gaussian_2pi(self):
        """ Test of a gaussian input 2pi soliton propagating through a two-level
            system.
        """
        json_path = os.path.join(JSON_DIR, "mbs_two_gaussian_2pi.json")
        mbs = mb_solve.MBSolve().from_json(json_path)
        mbs.mbsolve()
        # Input pulse is 2pi
        self.assertAlmostEqual(mbs.fields_area()[0][0]/(np.pi), 2.0, places=1)
        # Output pulse is 2pi
        self.assertAlmostEqual(mbs.fields_area()[0][-1]/(np.pi), 2.0, places=1)

    def test_two_gaussian_2pi_n_pi(self):
        """ Test of a gaussian input 2pi soliton propagating through a two-level
            system.
        """
        json_path = os.path.join(JSON_DIR, "mbs_two_gaussian_2pi_n_pi.json")
        mbs = mb_solve.MBSolve().from_json(json_path)
        mbs.mbsolve()
        # Input pulse is 2pi
        self.assertAlmostEqual(mbs.fields_area()[0][0]/(np.pi), 2.0, places=1)
        # Output pulse is 2pi
        self.assertAlmostEqual(mbs.fields_area()[0][-1]/(np.pi), 2.0, places=1)

    def test_two_sech_2pi(self):
        """ Test of a 2pi soliton propagating through a two-level system.
        """
        json_path = os.path.join(JSON_DIR, "mbs_two_sech_2pi.json")
        mbs = mb_solve.MBSolve().from_json(json_path)
        mbs.mbsolve()
        # Input pulse is 2pi
        self.assertAlmostEqual(mbs.fields_area()[0][0]/(np.pi), 2.0, places=1)
        # Output pulse is 2pi
        self.assertAlmostEqual(mbs.fields_area()[0][-1]/(np.pi), 2.0, places=1)

    def test_two_sech_2pi_n_pi(self):
        """ Test of a 2pi soliton propagating through a two-level system,
            passing n_pi.
        """
        json_path = os.path.join(JSON_DIR, "mbs_two_sech_2pi_n_pi.json")
        mbs = mb_solve.MBSolve().from_json(json_path)
        mbs.mbsolve()
        # Input pulse is 2pi
        self.assertAlmostEqual(mbs.fields_area()[0][0]/(np.pi), 2.0, places=1)
        # Output pulse is 2pi
        self.assertAlmostEqual(mbs.fields_area()[0][-1]/(np.pi), 2.0, places=1)

    def test_no_vel_classes(self):
        """ Empty velocity class dict. """

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mbs = mb_solve.MBSolve().from_json(json_path)

        vc = {}

        mbs.build_velocity_classes(vc)
        mbs.mbsolve()

    def test_no_vel_classes_inner(self):
        """ No inner delta values in dict. TODO: No mbsolve, should be init"""

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mbs = mb_solve.MBSolve().from_json(json_path)

        vc = {
            "thermal_delta_min": -1.0,
            "thermal_delta_max": 1.0,
            "thermal_delta_steps": 2,
            "thermal_width": 1.0
        }

        mbs.build_velocity_classes(vc)
        mbs.mbsolve()

    def test_zero_thermal_width(self):
        """TODO: No mbsolve, should be in init"""
        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mbs = mb_solve.MBSolve().from_json(json_path)

        vc = {
            "thermal_delta_min": -1.0,
            "thermal_delta_max": 1.0,
            "thermal_delta_steps": 2,
            "thermal_delta_inner_min": 0.0,
            "thermal_delta_inner_max": 0.0,
            "thermal_delta_inner_steps": 0,
            "thermal_width": 0.0
        }

        self.assertRaises(ValueError, mbs.build_velocity_classes, vc)

    def test_vel_classes(self):
        """Tests that for a linear two-level system with velocity classes, the
        absorption matches the known Voigt profile.
        """
        json_path = os.path.join(JSON_DIR, "velocity-classes.json")
        mbs = mb_solve.MBSolve().from_json(json_path)
        mbs.mbsolve()
        freq_list = spectral.freq_list(mbs)
        abs = spectral.absorption(mbs, 0, -1)
        voigt = spectral.voigt_two_linear_known(freq_list, 1.0, 0.05).imag
        # Assert that the max of the abs residuals between the absorption
        # profile and the known broadened Voigt absorption profile for linear 
        # two-level systems is below a tolerance
        self.assertTrue(np.max(np.abs(abs - voigt)) < 0.05)

class TestSaveLoad(unittest.TestCase):
    """ Tests for the MBSolve save and load methods. """

    def test_save_load_01(self):
        """ Solve a basic MBSolve problem. Save the results to file. Set the
            results in the MBSolve object to null. Load the results from
            file and check that they equal the original values.
        """

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mb_solve_01 = mb_solve.MBSolve().from_json(json_path)

        Omegas_zt, states_zt = mb_solve_01.mbsolve()

        mb_solve_01.save_results()

        mb_solve_01.Omegas_zt = None
        mb_solve_01.states_zt = None

        mb_solve_01.load_results()

        Omegas_zt_loaded = mb_solve_01.Omegas_zt
        states_zt_loaded = mb_solve_01.states_zt

        self.assertTrue((Omegas_zt == Omegas_zt_loaded).all())
        self.assertTrue((states_zt == states_zt_loaded).all())

    def test_save_load_no_recalc(self):

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mb_solve_01 = mb_solve.MBSolve().from_json(json_path)

        Omegas_zt, states_zt = mb_solve_01.mbsolve()

        mb_solve_01.save_results()

        mb_solve_01.Omegas_zt = None
        mb_solve_01.states_zt = None

        Omegas_zt, states_zt = mb_solve_01.mbsolve(recalc=False)

        Omegas_zt_loaded = mb_solve_01.Omegas_zt
        states_zt_loaded = mb_solve_01.states_zt

        self.assertTrue((Omegas_zt == Omegas_zt_loaded).all())
        self.assertTrue((states_zt == states_zt_loaded).all())

class TestBuildZlist(unittest.TestCase):

    def test_00(self):

        mb_solve_00 = mb_solve.MBSolve()

        zlist = np.array([0., .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.])

        self.assertTrue(np.allclose(mb_solve_00.zlist, zlist, rtol=1.0e-6))

class TestGetOmegasIntpTFuncs(unittest.TestCase):
    """ Unit tests of the get_Omegas_intp_t_funcs method """
    def test_one_field(self):
        """ For the case of a single field """

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mb_solve_00 = mb_solve.MBSolve().from_json(json_path)

        self.assertEqual(mb_solve_00.get_Omegas_intp_t_funcs(),
                         ['intp'])

    def test_two_fields(self):
        """ For the case of two fields """

        json_path = os.path.join(JSON_DIR, "mb_solve_lamda.json")
        mb_solve_lamda = mb_solve.MBSolve().from_json(json_path)

        self.assertEqual(mb_solve_lamda.get_Omegas_intp_t_funcs(),
                         ['intp', 'intp'])

class TestGetOmegasIntpTArgs(unittest.TestCase):
    """ Unit tests of the get_Omegas_intp_t_args method """

    def test_one_field(self):
        """ For the case of a single field """

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mb_solve_00 = mb_solve.MBSolve().from_json(json_path)

        Omegas_z =  mb_solve_00.Omegas_zt[:, 0, :]

        t_args = mb_solve_00.get_Omegas_intp_t_args(Omegas_z)

        self.assertEqual(len(t_args), 1)

        self.assertTrue(np.all(t_args[0]['tlist'] == mb_solve_00.tlist))
        self.assertTrue(np.all(t_args[0]['ylist'] == Omegas_z/(2.0*np.pi)))

class TestPopulations(unittest.TestCase):

    def test_twolevel_shape(self):

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mbs = mb_solve.MBSolve().from_json(json_path)

        pop_lower = mbs.populations([0])
        pop_upper = mbs.populations([1])

        np.testing.assert_allclose(pop_lower, np.zeros((mbs.z_steps+1, 
            mbs.t_steps+1)))
        np.testing.assert_allclose(pop_upper, np.zeros((mbs.z_steps+1, 
            mbs.t_steps+1)))

class TestPopulationsField(unittest.TestCase):

    def test_twolevel_shape(self):

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mbs = mb_solve.MBSolve().from_json(json_path)

        pop_upper = mbs.populations_field(field_idx=0, upper=True)
        pop_lower = mbs.populations_field(field_idx=0, upper=False)

        np.testing.assert_allclose(pop_lower, np.zeros((mbs.z_steps+1, 
            mbs.t_steps+1)))
        np.testing.assert_allclose(pop_upper, np.zeros((mbs.z_steps+1, 
            mbs.t_steps+1)))

class TestCoherences(unittest.TestCase):

    def test_twolevel_shape(self):

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mbs = mb_solve.MBSolve().from_json(json_path)
        coh = mbs.coherences([[0, 1]])

        np.testing.assert_allclose(coh, np.zeros((mbs.z_steps+1, 
            mbs.t_steps+1)))

class TestCoherencesField(unittest.TestCase):

    def test_twolevel_shape(self):

        json_path = os.path.join(JSON_DIR, "mb_solve_01.json")
        mbs = mb_solve.MBSolve().from_json(json_path)
        coh = mbs.coherences_field(field_idx=0)
        
        np.testing.assert_allclose(coh, np.zeros((mbs.z_steps+1, 
            mbs.t_steps+1)))
