import json
import os


def clean_before_test():
    """Clean up analysis logs before tests"""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    flake8_log = os.path.join(root_dir, 'flake8.log')
    radon_log = os.path.join(root_dir, 'radon.log')

    _trancate_file(flake8_log)
    _trancate_file(radon_log)


def _trancate_file(file_path):
    file = open(file_path, "r+")
    file.truncate(0)
    file.close()


def check_quality():
    """Analyse code quality"""
    before = _read_before_dict()
    new_flake8 = _get_new_flake8_stats()
    new_mi = _get_new_mi_stats()

    if len(before) != 0:
        assert int(before["flake8"]) >= new_flake8,\
            "You have introduced new pip8 errors. " \
            "Please check flake8.log for details. " \
            "Please fix all new and maybe some old errors"
        assert float(before["mi"]) <= new_mi, \
            "You have made code less maintainable. " \
            "Please check radon.log for details. " \
            "Please improve maintainability back. " \
            "Appreciate if you make it even better. "

    _save_new_results(new_flake8, new_mi)

    assert True, "Good work!"


def _read_before_dict():
    before_dict = dict()
    root_dir = os.path.dirname(os.path.abspath(__file__))
    project_quality = os.path.join(root_dir, "project_quality.txt")

    if os.path.exists(project_quality):
        for l in open(project_quality):
            if not l.startswith("#"):
                k, v = l.rstrip().split('=')
                before_dict[k] = v

    return before_dict


def _get_new_flake8_stats():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    flake8_log = os.path.join(root_dir, 'flake8.log')
    return len(open(flake8_log).readlines())


def _get_new_mi_stats():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    radon_log = os.path.join(root_dir, 'radon.log')
    radon_log_file = open(radon_log)
    radon_dict = json.load(radon_log_file)
    mi_scores = 0

    for stat in radon_dict.items():
        mi_scores += float(stat[1]["mi"])

    return mi_scores / len(radon_dict)


def _save_new_results(new_flake8, new_mi):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    project_quality = os.path.join(root_dir, "project_quality.txt")
    file = open(project_quality, "w")
    file.truncate(0)
    file.write(f"# Goal is '0'\nflake8={new_flake8}\n")
    file.write(f"# Goal is '100'\nmi={new_mi}\n")
