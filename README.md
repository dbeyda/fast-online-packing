# Fast Online Packing
Implementation of Agrawal &amp; Devanur's Online Stochastic Packing Algorithm, described in "Fast Algorithms for Online Stochastic Convex Programming".


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
  <h2 align="center">Fast Online Packing</h2>

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

This is an implementation of the 
Here's a blank template to get started...

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

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

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
pytest . > file.txt
```

<br />

### Generating New Documentation

Documentation is provided in the HTML format and was generated with [Sphinx](https://www.sphinx-doc.org/). API reference was generated automatically with [autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) from _docstrings_. Documentation source files are found in the `docs_src` folder.

To generate new documentation:
```
cd docs_src
make html
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