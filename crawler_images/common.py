def is_selected_model(model_name, model_names):
    selected = False
    mnl = model_name.lower()
    for mn in model_names:
        if mn in mnl:
            selected = True
            break
    return selected
