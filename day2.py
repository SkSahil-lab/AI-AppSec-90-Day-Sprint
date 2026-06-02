text = "python"
ans1 = text[0:3]
print(ans1)

text = "programming "
ans2 =text[-4:]
print(ans2)

text = "Data Science"
ans3 = text[::-1]
print(ans3)

msg = " Hello World "
ans4= msg.strip()
print(ans4)

word = "python"
ans5 = word.upper()
print(ans5)

sentence = "i like java"
ans6 = sentence.replace("java", "python")
print(ans6)

fruits = "apple,banana,mango"
ans7 = fruits.split(",")
print(ans7)

name = "shaik"
ans8 = name.startswith("sh")
print(ans8)

code = "abc123"
ans9 = code.isalnum()
print(ans9)

words = ["Learn", "Python", "Programming"]
ans10 = " ".join(words)
print(ans10)
