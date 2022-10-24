% monalysa documentation master file, created by
% sphinx-quickstart on Sat Oct 22 11:49:55 2022.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.

# Welcome to monalysa's documentation!

Monalysa -- **Mo**vement A**naly**sis libr**a**y is a python-based movement analysis
that provides a list of classes and fucntions for representing and analysing
movement related data from different technologies (motion capture, inertial
measurement units, robots, force/torque sensors, force plates, etc.). This
libary is aimed at students, reseachers, clinicians and industry professionals
working with movement analysis data.

```{important}
This docume ntation was generated on {{ today }}, and is updated regularly.
```

# Installation

You can easily install the library using pip:

```
pip install monalysa
```

# Exploration

The {doc}`kitchen-sink/index` section contains pages that contains basically
everything that you can with Sphinx "out-of-the-box".

```{toctree}
:titlesonly: true

Introduction <intro>
File Readers <reader>
UL Functioning <ulfunc>
```

Browsing through that section should give you a good idea of how stuff looks
in this theme.

# Navigation

This is the most important part of a documentation theme. If you like
the general look of the theme, please make sure that it is possible to
easily navigate through this sample documentation.

Ideally, the pages listed below should also be reachable via links
somewhere else on this page (like the sidebar, or a topbar). If they are
not, then this theme might need additional configuration to provide the
sort of site navigation that's necessary for "real" documentation.

Some pages like {doc}`placeholder-three` are declared in a "hidden"
toctree, and thus would not be visible above. However, they are still a
part of the overall site hierarchy and some themes may choose to present
them to the user in the site navigation.

______________________________________________________________________

[^id1]: If you hit an error while building documentation with a new theme,
    it is likely due to some theme-specific configuration in the `conf.py`
    file of that documentation. These are usually `html_sidebars`,
    `html_theme_path` or `html_theme_config`. Unsetting those will likely
    allow the build to proceed.

% Indices and tables

% ==================

% * :ref:`genindex`

% * :ref:`modindex`

% * :ref:`search`
