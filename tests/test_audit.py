import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import gen_orders, audit

class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p = os.path.join(tempfile.mkdtemp(), "o.csv"); gen_orders.generate(p); cls.res = audit.audit(p)
    def test_defect_found(self): self.assertEqual(len(self.res["product defect: free shipping not applied"]), 5)
    def test_policy_question_found(self): self.assertEqual(len(self.res["policy question: is the threshold checked before or after discount?"]), 8)
    def test_estimator_config_mismatch_is_only_canada(self):
        k = "configuration: estimator quote differs from billing (CA missing from estimator rates)"
        self.assertGreater(len(self.res[k]), 0); self.assertEqual(len(self.res), 3)
if __name__ == "__main__": unittest.main()
