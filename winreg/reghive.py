from regipy.registry import *

@attr.s
class GUI_Subkey(Subkey):
    subkey_count = attr.ib(type=int, kw_only=True)
    parent_path = attr.ib(type=str, kw_only=True)

class RegHive(RegistryHive):

    def recurse_subkeys(self, nk_record=None, path=None, parent=None, as_json=False):

        # If None, will start iterating from Root NK entry
        if not nk_record:
            nk_record = self.root

            # Get the values of the subkey
            values = []
            if nk_record.values_count:
                values = list(nk_record.iter_values(as_json=as_json))
            ts = convert_wintime(nk_record.header.last_modified)

            yield GUI_Subkey(subkey_name=nk_record.name, path="\\",
                         timestamp=ts.isoformat() if as_json else ts, values=values, values_count=len(values),
                         actual_path=f'{self.partial_hive_path}\\{subkey_path}' if self.partial_hive_path else None,
                         subkey_count=nk_record.header.subkey_count,
                         parent_path='')

        # Iterate over subkeys
        if nk_record.header.subkey_count:
            for subkey in nk_record.iter_subkeys():
                if path:
                    subkey_path = r'{}\{}'.format(path, subkey.name) if path else r'\{}'.format(subkey.name)
                    parent_path = path
                else:
                    subkey_path = f'\\{subkey.name}'
                    parent_path = "\\"
                # Leaf Index records do not contain subkeys
                if isinstance(subkey, LIRecord):
                    continue
                
                values = []
                if subkey.values_count:
                        values = list(subkey.iter_values(as_json=as_json))
                ts = convert_wintime(subkey.header.last_modified)
                yield GUI_Subkey(subkey_name=subkey.name, path=subkey_path,
                             timestamp=ts.isoformat() if as_json else ts, values=values,
                             values_count=len(values),
                             actual_path=f'{self.partial_hive_path}{subkey_path}' if self.partial_hive_path else None,
                             subkey_count=subkey.subkey_count,
                             parent_path=parent_path)

                if subkey.subkey_count:
                    yield from self.recurse_subkeys(nk_record=subkey,
                                                    path=subkey_path,
                                                    as_json=as_json)