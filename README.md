<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
  <h1 align="center">Fast Online Packing</h1>

  <p align="center">
    An implementation of Agrawal &amp; Devanur's Online Stochastic Packing Algorithm, described in "Fast Algorithms for Online Stochastic Convex Programming".
    <br />
    <a href="https://dbeyda.github.io/fast-online-packing/"><strong>Explore the docs »</strong></a>
  </p>
</p>
<br />
<br />




<!-- ABOUT THE PROJECT -->
## About The Project

This is an implementation of the [Online Packing](https://dbeyda.github.io/fast-online-packing/) algorithm presented by Agrawal  &amp; Devanur on ["Fast Algorithms for Online Stochastic Convex Programming"](https://dl.acm.org/doi/10.5555/2722129.2722222) (Algorithm 6.1), published in SODA'15. This algorithm tries to solve the Online Packing problem in the random-order model. [You can learn more about it in the docs](https://dbeyda.github.io/fast-online-packing/).


This project aims to provide a clear understanding of the algorithm, enlighten possible implementation dificulties and be used in fast prototyping scenarios. It was not designed for runtime performance nor for use in production environments.

In addition, this library provides a `Packing Problem` module that describes and enforces the Online Packing problem. This module can be used independently to assist the development of other algorithms for this same problem.  


### External Usage Dependencies

* [Python-MIP](https://www.python-mip.com/)
* [Google ORTools](https://developers.google.com/optimization)


<br />

<!-- GETTING STARTED -->
## Installation

First, check that you have Python 3.9+:
```
python3 --version
```

 Then, you can install the library with the following command:

```sh
pip install fast-online-packing
```


<br />

<!-- USAGE EXAMPLES -->
## Usage

<br />

```python
from fast_online_packing import instance_generator as generator
from fast_online_packing.online_solver import OnlineSolver

n_instants = 400
cost_dim = 5

delta = 0.3
values, costs, cap, e = generator.generate_valid_instance(
    delta, n_instants, cost_dim, items_per_instant=3)

# instantiate the solver
s = OnlineSolver(cost_dim, n_instants, cap, e, PythonMIPSolver)

for v, c in zip(values, costs):
    # ask the solver which item should we pack
    chosen_idx = s.pack_one(v, c)
    
    if chosen_idx == -1:
      print("No item chosen this round.")
    else:
      print("Algorithm picked item with index ", chosen_idx)
      item_value = v[chosen_idx]
      item_cost_vector = c[chosen_idx]
```

_For more examples, please refer to the [Documentation](https://dbeyda.github.io/fast-online-packing/)_


<br />

<!-- Further Development -->
## Further Development / Contributing

Clone the repo somewhere inside your project:
```
git clone https://github.com/dbeyda/fast-online-packing
```

Install development dependencies:
```
pip install -r fast-online-learning/requirements.txt
```

Install the cloned repo using the `--editable` option:
```
pip install -e <path/to/fast-online-packing>
```

Develop, develop, develop. When you're finished, make to update and run the **tests**, and update and generate new **docs**. 

<br />

### Tests
Tests were developed using [PyTest](https://pytest.org/). There is one test for each module, all located under the `tests/` folder.

To run all tests, use the following command:
```
pytest .
```

If you want to output the test log to a file, you can do:
```
pytest . > testlog.txt
```

<br />

### Generating New Documentation

Documentation is provided in the HTML format and was generated with [Sphinx](https://www.sphinx-doc.org/). API reference was generated automatically with [autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) from _docstrings_. Documentation source files are found in the `docs_src` folder, and generated HTML docs are in the `docs/` folder. This arrangement facilitates deploying the docs to GitHub Pages. 

To generate new documentation:
```
cd docs_src
make github
```

Sphinx will read the `.rst` files in `docs_src/` to generate new HTML files in the `docs/` folder.

<br />

---

<br />

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<br />

<!-- CONTACT -->
## Contact

David Beyda - dbeyda@poli.ufrj.br

Project Link: [https://github.com/dbeyda/fast-online-packing](https://github.com/dbeyda/fast-online-packing)


<br />

<!-- DISCLAIMER -->
## Disclaimer
This package was implemented as the Final Programming Assignment of my Msc. in PUC-Rio. It was developed only by me. This project is an independent work. It is **not** the original / official implementation of Agrawal &amp; Devanur's paper. 


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/dbeyda/repo.svg?style=for-the-badge
[license-url]: https://github.com/dbeyda/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/david-beyda/