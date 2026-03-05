import re


def get_model_name(model_name):
    index = model_name.rfind("/")
    model_name = model_name[:index]
    model_name = re.sub(r'[?/\'|.]', '', model_name)
    return model_name.strip()

print(get_model_name("fasdfa / Duo"))
print(get_model_name("fasdfa / Solo"))