def encode(s):
    buffer = ''
    phrases = {}
    ans = []
    for i in range(len(s)):
        if phrases.get(buffer + s[i]) != None:
            buffer += s[i]
        else:
            key = phrases.get(buffer)
            if key == None:
                key = 0
            ans.append((key, s[i]))
            phrases[buffer + s[i]] = len(phrases) + 1
            buffer = ''
    print(phrases)
    return ans

print(encode('abacababacabc'))