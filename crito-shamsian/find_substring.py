
A = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

def skip_substring(A, B):
    print(" ".join(B), end=" ")
    found = False

    matches = []
    for i in range(1, len(B) + 1):
        found = False
        if matches:
            start = matches[-1]
        else:
            start = 1
        for j in range(start, len(A) + 1):
            if A[j - 1] == B[i - 1]:
                matches.append(j)
                found = True
                break
        if found:
            continue
        else:
            matches = None
            break

    print(matches)

find_substring(A, ["A", "B", "C"])
find_substring(A, ["C", "D", "E"])
find_substring(A, ["C", "D", "G", "H"])
find_substring(A, ["C", "D", "H", "G"])

