from app.core import db

GROUPS = ['sum', 'avg', 'count']
FILTERS = ['$gt', '$lt', '$eq']
PERIODS = ['year', 'month', 'week', 'day', 'hour', 'minute', 'second']
ORDERS = ['asc', 'desc']


def run_query_on(query_object, field_provider, **kwargs):
    selections, filters, groups, orderings = validate_selections(**kwargs)
    entities = []

    print('Starting with args: ' + str(kwargs))

    if selections is not None:
        if groups is not None:
            for group in groups.keys():
                entities.append(
                        get_group(
                            field_provider(group),
                            groups[group]
                            ).label(
                                'group_' + str(group)  # + '_' + groups[group]
                                )
                            )

        for selection in selections.keys():
            entities.append(get_column(selections[selection],
                            field_provider(selection)).label(selection))

        print('New entities: ' + str(entities))
        query_object = query_object.with_entities(*entities)

    if filters is not None:
        for filtered_column in filters.keys():
            for actual_filter in filters[filtered_column].keys():
                query_object = query_object.filter(
                        get_filter(field_provider(filtered_column),
                                   actual_filter,
                                   filters[filtered_column][actual_filter]))

    if groups is not None:
        for group in groups.keys():
            query_object = query_object.group_by('group_' + str(group))

    if orderings is not None:
        for order in orderings.keys():
            if ((selections is not None and
                    order not in selections.keys())
                    and
                    (groups is None or
                        order not in ['group_' + str(group) for group in
                                      groups.keys()])):
                            raise ValueError(
                                    'Invalid order! Must use one of' +
                                    ' selections or groups')
            query_object = query_object.order_by(
                    order + ' ' + orderings[order])

    return query_object


def get_column(selection_name, field):
    if selection_name == 'value':
        return field
    if selection_name == 'sum':
        return db.func.sum(field)
    if selection_name == 'avg':
        return db.func.avg(field)
    if selection_name == 'count':
        return db.func.count(field)


def get_filter(filter_column, filter_key, filter_value):
    if filter_key == '$gt':
        return filter_column > filter_value
    if filter_key == '$lt':
        return filter_column < filter_value
    if filter_key == '$eq':
        return filter_column == filter_value


def get_group(group_column, group_value):
    if group_value == 'value':
        return group_column
    if group_value in PERIODS:
        return db.func.date_part(group_value, group_column)
    # We now expect a date format
    return db.func.to_char(group_column, group_value)


def is_group(**kwargs):
    if kwargs.get('group') is not None:
        return True


def validate_selections(**kwargs):
    selections = kwargs.get('selections')
    filters = kwargs.get('filters')
    groups = kwargs.get('groups')
    orderings = kwargs.get('orders')

    if selections is None:
        raise ValueError("Missing selections!")

    if is_group(**kwargs):
        for key in selections.keys():
            if selections[key] not in GROUPS:
                raise ValueError("Can only use " + str(GROUPS) + " when " +
                                 "grouping!")

    if filters is not None:
        for key in filters.keys():
            for inner_key in filters[key].keys():
                if inner_key not in FILTERS:
                    raise ValueError("Invalid filter (" + str(
                        inner_key) + "). Valid filters: " + str(FILTERS))

    if orderings is not None:
        for key in orderings.keys():
            if orderings[key] not in ORDERS:
                raise ValueError("Invalid order type ("
                                 + orderings[key] + "). " +
                                 "Valid types: " + str(ORDERS))

    return selections, filters, groups, orderings
