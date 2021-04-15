def inspect_project(p, sample_names=None, max_attr=10):
    """
    Print inspection info: Project or,
    if sample_names argument is provided, matched samples

    :param peppy.Project p: project to inspect
    :param Iterable[str] sample_names: list of samples to inspect
    :param int max_attr: max number of sample attributes to display
    """
    if sample_names:
        samples = p.get_samples(sample_names)
        if not samples:
            print("No samples matched by names: {}".format(sample_names))
            return
        for s in samples:
            print(s.__str__(max_attr=max_attr))
            print("\n")
        return
    print(p)
    return
