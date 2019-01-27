import sys
import os
from itertools import zip_longest
from glob import glob


def checkDiffs(path1, path2):
    def diffFeature(f):
        with open(f'{path1}/{f}.tf') as h:
            eLines = (
                h.readlines()
                if f == 'otext' else
                (d for d in h.readlines() if not d.startswith('@'))
            )
        with open(f'{path2}/{f}.tf') as h:
            nLines = (
                h.readlines()
                if f == 'otext' else
                (d for d in h.readlines() if not d.startswith('@'))
            )
        i = 0
        equal = True
        cutOff = 40
        limit = 4
        nUnequal = 0
        for (e, n) in zip_longest(eLines, nLines, fillvalue='<empty>'):
            i += 1
            if e != n:
                if nUnequal == 0:
                  print(
                      'differences{}'.format(
                          '' if f == 'otext' else ' after the metadata'
                      )
                  )
                shortE = e[0:cutOff] + (' ...' if len(e) > cutOff else '')
                shortN = n[0:cutOff] + (' ...' if len(n) > cutOff else '')
                print('\tline {:>6} OLD -->{}<--'.format(i, shortE.rstrip('\n')))
                print('\tline {:>6} NEW -->{}<--'.format(i, shortN.rstrip('\n')))
                equal = False
                nUnequal += 1
                if nUnequal >= limit:
                  break

        print('no changes' if equal else '')

    print(f'Check differences between TF files in {path1} and {path2}')
    files1 = glob(f'{path1}/*.tf')
    files2 = glob(f'{path2}/*.tf')
    features1 = {os.path.basename(os.path.splitext(f)[0]) for f in files1}
    features2 = {os.path.basename(os.path.splitext(f)[0]) for f in files2}

    addedOnes = features2 - features1
    deletedOnes = features1 - features2
    commonOnes = features2 & features1

    if addedOnes:
        print(f'\t{len(addedOnes)} features to add')
        for f in sorted(addedOnes):
          print(f'\t\t{f}')
    else:
        print(f'\tno features to add')
    if deletedOnes:
        print(f'\t{len(deletedOnes)} features to delete')
        for f in sorted(deletedOnes):
          print(f'\t\t{f}')
    else:
        print(f'\tno features to delete')

    print(f'\t{len(commonOnes)} features in common')
    for f in sorted(commonOnes):
      print(f'{f}')
      diffFeature(f)
    print('Done')


checkDiffs(*sys.argv[1:3])
