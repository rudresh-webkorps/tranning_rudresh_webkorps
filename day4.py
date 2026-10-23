def count_up(n):
    i = 1
    print("Counting up to", n)
    while i <= n:
        yield i
        i += 1

# for x in count_up(3):
#     print(x)   

x = count_up(3)
print(x)
