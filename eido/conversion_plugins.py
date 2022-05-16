""" built-in PEP filters """
from typing import Dict


def basic_pep_filter(p, **kwargs) -> Dict[str, str]:
    """
    Basic PEP filter, that does not convert the Project object.

    This filter can save the PEP representation to file, if kwargs include `path`.

    :param peppy.Project p: a Project to run filter on
    """
    return {"project": str(p)}


def yaml_samples_pep_filter(p, **kwargs) -> Dict[str, str]:
    """
    YAML samples PEP filter, that returns only Sample object representations.

    This filter can save the YAML to file, if kwargs include `path`.

    :param peppy.Project p: a Project to run filter on
    """
    from yaml import dump

    samples_yaml = []
    for s in p.samples:
        samples_yaml.append(s.to_dict())

    return {"samples": dump(samples_yaml, default_flow_style=False)}


def yaml_pep_filter(p, **kwargs) -> Dict[str, str]:
    """
    YAML PEP filter, that returns Project object representation.

    This filter can save the YAML to file, if kwargs include `path`.

    :param peppy.Project p: a Project to run filter on
    """
    from yaml import dump

    data = p.config.to_dict()
    return {"project": dump(data, default_flow_style=False)}


def csv_pep_filter(p, **kwargs) -> Dict[str, str]:
    """
    CSV PEP filter, that returns Sample object representations

    This filter can save the CSVs to files, if kwargs include
    `sample_table_path` and/or `subsample_table_path`.

    :param peppy.Project p: a Project to run filter on
    """
    sample_table_path = kwargs.get("sample_table_path")
    subsample_table_path = kwargs.get("subsample_table_path")
    sample_table_repr = p.sample_table.to_csv(path_or_buf=sample_table_path)

    s = ""
    if sample_table_repr is not None:
        s += sample_table_repr
    if p.subsample_table is not None:
        subsample_table_repr = p.subsample_table.to_csv(
            path_or_buf=subsample_table_path
        )
        if subsample_table_repr is not None:
            s += subsample_table_repr

    return {"samples": s}


def processed_pep_filter(p, **kwargs) -> Dict[str, str]:
    """
    Processed PEP filter, that returns the converted sample and subsample tables.
    This filter can return the tables as a table or a document.
    :param peppy.Project p: a Project to run filter on
    :param bool samples_as_objects: Flag to write as a table
    :param bool subsamples_as_objects: Flag to write as a table
    """
    # get params
    samples_as_objects = kwargs.get("samples_as_objects")
    subsamples_as_objects = kwargs.get("subsamples_as_objects")

    prj_repr = p.config.to_dict()

    return {
        "project": str(prj_repr),
        "samples": str(p.samples)
        if samples_as_objects
        else str(p.sample_table.to_csv()),
        "subsamples": str(p.subsamples)
        if subsamples_as_objects
        else str(p.subsample_table.to_csv()),
    }
