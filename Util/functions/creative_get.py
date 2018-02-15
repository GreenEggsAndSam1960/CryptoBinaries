def creative_get(model, comparison):
    fields = model._meta.get_fields()
    unique_fields = [field for field in fields if getattr(field, 'unique', False)]

    search = {}

    for field in unique_fields:
        try:
            search[field.name] = comparison[field.name]
            break
        except KeyError:
            pass

    if not search:
        raise ValueError('No matching unique field found')

    try:
        return model.objects.get(**search)
    except model.DoesNotExist:
        instance = model()

        for field in comparison:
            instance.__setattr__(field, comparison[field])

        instance.save()
        print('Added %s to %s model' % (instance.__str__(), model.__name__))
        return instance
