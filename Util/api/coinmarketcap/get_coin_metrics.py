from typing import Union

from .config import base_url, valid_currencies
from ..methods import get

def _get_individual(cmc_id: str, convert: str=None):
    params = {}

    if convert in valid_currencies:
        params['convert'] = convert

    return get(
        '%sticker/%s/' % (base_url, cmc_id),
        params=params
    )

def _get_collection(convert: str='', start: int=-1, limit: int=-1):
    params = {}

    if convert in valid_currencies:
        params['convert'] = convert
    if start >= 0:
        params['start'] = int(start)
    if limit >= 0:
        params['limit'] = int(limit)

    return get(
        base_url + 'ticker/',
        params=params
    )

def _get_multi_conversion(convert: list, cmc_id: str=None, start: int=-1, limit: int=-1):
    if len(convert) > 5:
        raise IndexError('Too many currencies to convert for')

    results = []
    for currency in convert:
        if cmc_id:
            response = _get_individual(cmc_id, convert=currency)['response']
        else:
            response = _get_collection(convert=currency, start=start, limit=limit)['response']

        if response:
            results.extend(response)

    return _merge_results(results, 'symbol')

def _merge_results(results: list, matching_key: str):
    merge_list = []
    key_index = {}

    for result in results:
        try:
            key = result[matching_key]
        except KeyError:
            key = False

        if key:
            try:
                index = key_index[key]
                merge_list[index] = {**merge_list[index], **result}
            except KeyError:
                key_index[key] = len(merge_list)
                merge_list.append(result)

    return merge_list

def get_coin_metrics(cmc_id: str=None, convert: Union[str, list]=None, start: int=-1, limit: int=-1):
    if cmc_id and type(convert) is list:
        return _get_multi_conversion(convert, cmc_id=cmc_id)
    elif cmc_id:
        return _get_individual(cmc_id, convert=convert)
    elif type(convert) is list:
        return _get_multi_conversion(convert=convert, start=start, limit=limit)
    else:
        return _get_collection(convert=convert, start=start, limit=limit)