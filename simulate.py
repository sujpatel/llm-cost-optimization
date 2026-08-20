import httpx

PROMPTS = {
    "coding": [
        "Write a Python function to reverse a linked list.",
        "Explain the difference between a list and a tuple in Python.",
        "Write a SQL query to find duplicate emails in a users table.",
        "Fix this bug: a for loop that off-by-one errors on the last index.",
        "Write a function to check if a string is a palindrome.",
        "Write a function to find the longest common substring of two strings.",
        "Explain the difference between a stack and a queue.",
        "Write a Python decorator that times how long a function takes.",
        "Explain what a race condition is and how to prevent one.",
        "Write a regex to validate an email address.",
    ],
    "intelligence": [
        "Explain the tradeoffs between microservices and monoliths.",
        "Summarize the main causes of the 2008 financial crisis.",
        "What are the pros and cons of remote work for a startup?",
        "Explain how a hash table works and why it's fast.",
        "Compare SQL and NoSQL databases for a social media app.",
        "Explain the CAP theorem in simple terms.",
        "What's the difference between latency and throughput?",
        "Explain how DNS resolution works step by step.",
        "Compare REST and GraphQL for a mobile app backend.",
        "Explain what eventual consistency means in distributed systems.",
    ],
    "agentic": [
        "Plan the steps to migrate a Postgres database with zero downtime.",
        "Break down how you'd debug a memory leak in production.",
        "Outline a plan to onboard a new engineer to a codebase.",
        "Describe steps to set up CI/CD for a Python project.",
        "Plan how to roll back a bad deployment safely.",
        "Outline steps to investigate a spike in API error rates.",
        "Plan a strategy to migrate a monolith to microservices incrementally.",
        "Describe how you'd plan a load test for a new API endpoint.",
        "Outline steps to respond to a production database outage.",
        "Plan how to safely rotate a leaked API key in production.",
    ],
}

BASE_URL = "http://127.0.0.1:8000"

total = sum(len(prompts) for prompts in PROMPTS.values())
count = 0

for task_type, prompts in PROMPTS.items():
    for prompt in prompts:
        count += 1
        print(f"[{count}/{total}] Sending ({task_type})...", flush=True)
        try:
            response = httpx.post(
                f"{BASE_URL}/v1/ask",
                json={"prompt": prompt, "task_type": task_type},
                timeout=120,
            )
            result = response.json()
            print(
                f"[{count}/{total}] {prompt[:40]}... -> {result.get('model_used', result.get('error'))}",
                flush=True,
            )
        except (httpx.HTTPError, ValueError) as e:
            print(f"[{count}/{total}] FAILED: {e}", flush=True)

print(flush=True)
savings = httpx.get(f"{BASE_URL}/v1/savings").json()
print("Final savings:", savings, flush=True)
