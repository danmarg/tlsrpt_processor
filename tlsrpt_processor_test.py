import unittest
import tlsrpt_processor

class TestParsesSample(unittest.TestCase):
  def test_rfc_sample(self):
    # TODO(abrotman): Check the output? ;)
    tlsrpt_processor.main(["-i", "testdata/sample.json", "-o", "kv"])


if __name__ == "__main__":
  unittest.main()
