import unittest

from kairos_echo import KairosEchoPrototype, SimulationConfig, audit_guardian


class VetoAuditTests(unittest.TestCase):
    def test_one_step_veto_penalty_can_lower_simulated_coherence(self):
        config = SimulationConfig(
            steps=1, initial_coherence=0.3, inward_probability=0.0,
            outward_mean=-0.04, outward_std=0.0,
        )
        result = audit_guardian(config, replicates=1)
        run = result["runs"][0]
        self.assertEqual(run["veto_count"], 1)
        self.assertAlmostEqual(run["final_coherence_with_veto"], 0.12)
        self.assertAlmostEqual(run["final_coherence_zero_penalty_veto"], 0.3)
        self.assertAlmostEqual(run["final_coherence_without_veto"], 0.26)
        self.assertAlmostEqual(result["mean_difference_with_minus_without"], -0.14)
        self.assertAlmostEqual(result["mean_difference_zero_penalty_minus_without"], 0.04)

    def test_paired_stream_and_repeated_audit_are_identical(self):
        config = SimulationConfig(seed=42, steps=80)
        with_veto = KairosEchoPrototype(config).run(veto_enabled=True)
        no_veto = KairosEchoPrototype(config).run(veto_enabled=False)
        self.assertEqual(with_veto["proposed_action"], no_veto["proposed_action"])
        self.assertEqual(with_veto["sampled_delta"], no_veto["sampled_delta"])
        self.assertEqual(sum(no_veto["vetoed"]), 0)
        self.assertEqual(audit_guardian(config, replicates=8), audit_guardian(config, replicates=8))

    def test_no_trigger_means_policies_agree(self):
        config = SimulationConfig(
            steps=4, initial_coherence=0.9, inward_probability=0.0,
            outward_mean=0.0, outward_std=0.0,
        )
        result = audit_guardian(config, replicates=2)
        self.assertEqual(result["mean_difference_with_minus_without"], 0.0)
        self.assertEqual(result["mean_difference_zero_penalty_minus_without"], 0.0)
        self.assertEqual([run["veto_count"] for run in result["runs"]], [0, 0])

    def test_existing_summary_still_works(self):
        simulator = KairosEchoPrototype(SimulationConfig(steps=4))
        simulator.run()
        self.assertEqual(simulator.summary().steps, 4)
        with self.assertRaises(ValueError):
            audit_guardian(SimulationConfig(), replicates=0)


if __name__ == "__main__":
    unittest.main()
