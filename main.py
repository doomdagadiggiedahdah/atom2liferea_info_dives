import subprocess as sub

link = "http://0.0.0.0:8000/q.atom"
result = sub.run(["liferea-add-feed", link], capture_output=True, text=True)

print(f"output: {result.stdout}")

if result.returncode == 0:
    print("all good")
else:
    print("didn't work")
