""" built-in PEP filters """
import sys


def basic_pep_filter(p, **kwargs):
    """
    Basic PEP filter, that does not convert the Project object.

    This filter can save the PEP representation to file, if kwargs include `path`.

    :param peppy.Project p: a Project to run filter on
    """
    path = kwargs.get("path")
    if path is not None:
        with open(path, "w") as text_file:
            text_file.write(p.__str__)
    else:
        print(p)


def yaml_samples_pep_filter(p, **kwargs):
    """
    YAML samples PEP filter, that returns only Sample object representations.

    This filter can save the YAML to file, if kwargs include `path`.

    :param peppy.Project p: a Project to run filter on
    """
    path = kwargs.get("path")
    if path is not None:
        from yaml import dump

        samples_yaml = []
        for s in p.samples:
            samples_yaml.append(s.to_dict())
        with open(path, "w") as outfile:
            dump(samples_yaml, outfile, default_flow_style=False)
    else:
        import re

        from yaml import safe_dump

        for s in p.samples:
            sys.stdout.write("- ")
            out = re.sub("\n", "\n  ", safe_dump(s.to_dict(), default_flow_style=False))
            sys.stdout.write(out + "\n")


def yaml_pep_filter(p, **kwargs):
    """
    YAML PEP filter, that returns Project object representation.

    This filter can save the YAML to file, if kwargs include `path`.

    :param peppy.Project p: a Project to run filter on
    """
    from yaml import dump

    path = kwargs.get("path")
    if path is not None:
        data = p.config.to_dict()
        with open(path, "w") as outfile:
            dump(data, outfile, default_flow_style=False)
    else:
        data = p.config.to_yaml()
        print(data)


def csv_pep_filter(p, **kwargs):
    """
    CSV PEP filter, that returns Sample object representations

    This filter can save the CSVs to files, if kwargs include
    `sample_table_path` and/or `subsample_table_path`.

    :param peppy.Project p: a Project to run filter on
    """
    sample_table_path = kwargs.get("sample_table_path")
    subsample_table_path = kwargs.get("subsample_table_path")
    sample_table_repr = p.sample_table.to_csv(path_or_buf=sample_table_path)
    if sample_table_repr is not None:
        sys.stdout.write(sample_table_repr)
    if p.subsample_table is not None:
        subsample_table_repr = p.subsample_table.to_csv(
            path_or_buf=subsample_table_path
        )
        if subsample_table_repr is not None:
            sys.stdout.write(subsample_table_repr)
