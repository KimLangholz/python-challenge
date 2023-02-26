import requests, time

BASE = "http://127.0.0.1:5000"

username = "dr_crocodile"

# First API call.

start_time = time.perf_counter()

response = requests.get(BASE + f"/api/v1.0/buildable-sets/{username}")

end_time = time.perf_counter()
execution_time = end_time - start_time

print(response.json())
print(f"The execution time is: {execution_time}")

# Next API call.

start_time = time.perf_counter()
response = requests.get(BASE + f"/api/v1.0/buildable-sets-additional/{username}")
end_time = time.perf_counter()
execution_time = end_time - start_time

print(response.json())
print(f"The execution time is: {execution_time}")