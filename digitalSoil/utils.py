import pandas as pd


def get_model_field_names(model, ignore_fields=['content_object']):
    """
    :param model: a django model class
    :param ignore_fields: is a list of field names to ignore by default
    :return: all model field names (as strings) and returns a list of them ignoring the ones we don't work (like
    the 'content_objects' field)
    """
    model_fields = model._meta.get_field()
    model_field_names = list(set([f.name for f in model_fields if f.name not in ignore_fields]))
    return model_field_names


def get_lookup_fields(model, fields=None):
    """

    :param models: a Django model class
    :param fields: is a list of field name strings.
    :return: This method compares the lookups we want vs the lookups that are avaulable. It gnores the unavailable
    fields we passed.
    """
    model_field_names = get_model_field_names(model)
    if fields is not None:
        """
        we'll iterate through all the passed fields)names
        and verify they are valid by only including the valid ones
        """
        lookup_fields = []
        for x in fields:
            if "__" in x:
                lookup_fields.append(x)
            elif x in model_field_names:
                lookup_fields.append(x)
    else:
        """
        No field names were passed, use the default model fields
        """
        lookup_fields = model_field_names
    return lookup_fields


def qs_to_dataset(qs, fields=None):
    """
    :param qs: is any Django queryset
    :param fields: list of field name strings, ignoring non-model field names
    :return: This method is the final step, simply calling the fields we fromed on the queryset
    and turning it into a list of dictionaries with key/value pairs.
    """
    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    return list(qs.values(*lookup_fields))


def convert_to_dataframe(qs, fields=None, index=None):
    """

    :param qs: a queryset from django
    :param fields: is a list of filed names from the Model of the Queryset
    :param index: is thee preferred index column we want out dataframe to be set to
    :return: Using the methods from above, we can easyly build a dataframe from this data.
    """
    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    index_col = None
    if index in lookup_fields:
        index_col = index
    elif "id" in lookup_fields:
        index_col = 'id'
    values = qs_to_dataset(qs, fields=fields)
    df = pd.DataFrame.from_records(values, columns=lookup_fields, index=index_col)
    return df

