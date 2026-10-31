"""Harness for the advanced mathematics reasoning and verification benchmark.

``models``          the ``problem.yaml`` schema
``verify_support``  helpers the per-problem ``verify.py`` scripts import
``runner``          runs every verification script and collects the results
``cli``             ``mathbench list | show | verify``

The harness deliberately keeps *verification* and *proof* in separate places.
``verify.py`` produces numerical and symbolic evidence at specific instances;
``solution.md`` carries the argument that covers every instance. See
``docs/verification-vs-proof.md`` for why the distinction is enforced rather
than left to taste.
"""

__version__ = "0.1.0"
