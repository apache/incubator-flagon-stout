import hashlib

def generateCode(uid, uhash):
    hash = hashlib.sha1()
    hash.update(uhash)
    part2 = hash.hexdigest()[15:-15]
    part1 = str(999999-(uid%1000000)).zfill(6)

    return part1+part2
