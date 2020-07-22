import os

def _df(part, verbose):
    free_kib = os.getfree(part)
    free_b = free_kib * 1024
    free_mib = free_kib / 1024
    if verbose:
        import ls
        used_b = ls.du(part, do_return=True)
        used_kib = used_b / 1024
        total_b = used_b + free_b
        total_kib = total_b / 1024
        error_b = 4 * 1024 * 1024 - total_b
        print(part, ' ', free_b, ' B free (', free_kib, " KiB, ", round(free_kib / 1024,2), " MiB), ", used_b, ' B used (', round(used_kib,2), ' KiB, ', round(used_kib / 1024,2), ' MiB), ', total_b, ' B total (', total_kib, ' KiB, ', round(total_kib / 1024,2), ' MiB) [error_b=', error_b, ']', sep='')
        # /flash 4087808 B free (3992 KiB, 3.9 MiB), 41247 B used (40.28 KiB, 0.04 MiB), 4129055 B total (4032.28 KiB, 3.94 MiB) [error_b=65249]
        # FIXME: why do we have an error of 64K?
        # I would expect something below 1K due to rounding since os.getfree() reports in KiB
        # probably something like inodes, ie managing directories and filenames
    else:
        print(part, kib * 1024, 'B free (', kib, "KiB)", sep='')

def df(part='', verbose=True):
    if part == '':
        _df("/flash", verbose)
        try:
            _df('/sd', verbose)
        except:
            pass
    else:
        _df(part, verbose)

if __name__ == "__main__":
    df()
