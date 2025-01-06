import toml
import yaml

with open("all_in_one.yaml") as fp:
    r = yaml.safe_load(fp)
r

r = toml.load("bessyii_family_info.toml")
r

with open("bessyii_family_info.yaml") as fp:
    r = yaml.safe_load(fp)
r

with open("conversion_factors.yaml") as fp:
    r = yaml.safe_load(fp)
r