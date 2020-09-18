[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4036587.svg)](https://doi.org/10.5281/zenodo.4036587)

About
-----

This project has made the following contributions,

1. A modified form of the Bi-section search algorithm first presented in [1] is implemented. The trends observed are as expected. See, `results/bi_search` directory.

2. An efficient local search algorithm is proposed which finds the offloading schemes which are very close to the optimal offloading schemes using very little computation efforts as compared to the search algorithms presented in [1].

3. Numerical benchmarking has been done on the basis of parameters used in [1] for each algorithm implemented to verify the correctness and to support our claims. See, `results/local_search` and See, `results/naive_search` directory.

Dependencies
------------

1. Python 3.6.9
2. Matplotlib 2.1.0

Testing
-------

Please follow the steps given below for running tests,

1. Change your directory the root of this repository that is, `/path/to/MECOptimalOffloading`.
2. Execute, `python3 mecoptimaloffloading/tests/test_[x]_search.py`, where `[x]` can be replaced by `bi` for testing Bi-section search implementation, `local` for testing local search algorithm, and `naive` for testing naive search algorithm.

You can modify the `config` which is `dict` python variable for changing the parameters according to the conditions. The keys use strings which are in accordance with the notations used in [1].

References
----------

[1] J. Yan, S. Bi, and Y. J. Zhang, “Optimal offloading and resource allocation in mobile-edge computing with inter-user task dependency,” accepted by IEEE GLOBECOM, Dec. 2018.
[2] Y. Mao, C. You, J. Zhang, K. Huang, and K. B. Letaief, “A survey on mobile edge computing: The communication perspective,” IEEE Commun. Surveys Tuts., vol. 19, no. 4, pp. 2322–2358, Fourthquarter 2017.
