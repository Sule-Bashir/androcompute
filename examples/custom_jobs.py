"""
Custom Job Definitions for AndroCompute
These job codes are executed on Android worker nodes
"""

# Job 1: Calculate Pi with Leibniz formula
CALCULATE_PI_JOB = """
import math
result = 0
for i in range(1000000):
    result += (-1) ** i / (2 * i + 1)
result = result * 4
"""

# Job 2: File Hash Calculator
HASH_FILE_JOB = """
import hashlib
test_data = "AndroCompute Distributed Computing Platform"
# Calculate multiple hashes
md5_hash = hashlib.md5(test_data.encode()).hexdigest()
sha256_hash = hashlib.sha256(test_data.encode()).hexdigest()
result = f"MD5: {md5_hash}, SHA256: {sha256_hash}"
"""

# Job 3: Mathematical Computation - Fibonacci
FIBONACCI_JOB = """
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

result = fibonacci(20)  # Calculate 20th Fibonacci number
"""

# Job 4: Prime Number Checker
PRIME_CHECKER_JOB = """
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Check first 50 numbers for primes
primes = [str(i) for i in range(2, 51) if is_prime(i)]
result = f"Primes up to 50: {', '.join(primes)}"
"""

# Job 5: Matrix Multiplication
MATRIX_MULTIPLY_JOB = """
import math
# Create sample matrices
matrix_a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
matrix_b = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]

# Perform matrix multiplication
result_matrix = []
for i in range(len(matrix_a)):
    row = []
    for j in range(len(matrix_b[0])):
        sum_val = 0
        for k in range(len(matrix_b)):
            sum_val += matrix_a[i][k] * matrix_b[k][j]
        row.append(sum_val)
    result_matrix.append(row)

result = f"Matrix result: {result_matrix}"
"""

# Job 6: Data Processing - Word Frequency
WORD_FREQUENCY_JOB = """
sample_text = '''
AndroCompute is a distributed computing platform that leverages Android devices.
It allows parallel processing across multiple mobile devices.
This enables large computations to be broken into smaller tasks.
'''

# Process text and count word frequencies
words = sample_text.lower().split()
word_count = {}
for word in words:
    # Clean word (remove punctuation)
    clean_word = ''.join(char for char in word if char.isalnum())
    if clean_word:
        word_count[clean_word] = word_count.get(clean_word, 0) + 1

# Get top 10 words
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]
result = f"Top 10 words: {dict(sorted_words)}"
"""

# Job 7: Mathematical Series Sum
SERIES_SUM_JOB = """
# Calculate sum of series: 1 + 1/2 + 1/4 + 1/8 + ... + 1/1024
series_sum = 0
for i in range(11):  # 2^10 = 1024
    series_sum += 1 / (2 ** i)
result = f"Series sum: {series_sum:.6f}"
"""

# Job 8: String Operations
STRING_OPERATIONS_JOB = """
text = "AndroCompute Distributed Computing Platform"

# Various string operations
operations = {
    'uppercase': text.upper(),
    'lowercase': text.lower(),
    'word_count': len(text.split()),
    'character_count': len(text),
    'reversed': text[::-1]
}

result = f"String analysis: {operations}"
"""

# Dictionary mapping job types to their code
JOB_TYPES = {
    'calculate_pi': CALCULATE_PI_JOB,
    'hash_file': HASH_FILE_JOB,
    'fibonacci': FIBONACCI_JOB,
    'prime_checker': PRIME_CHECKER_JOB,
    'matrix_multiply': MATRIX_MULTIPLY_JOB,
    'word_frequency': WORD_FREQUENCY_JOB,
    'series_sum': SERIES_SUM_JOB,
    'string_operations': STRING_OPERATIONS_JOB
}

def get_job_code(job_type):
    """
    Get the executable Python code for a job type
    
    Args:
        job_type (str): Type of job to execute
        
    Returns:
        str: Python code to execute on worker node
    """
    return JOB_TYPES.get(job_type, 'result = "Unknown job type"')

def list_available_jobs():
    """
    Return list of all available job types
    """
    return list(JOB_TYPES.keys())

if __name__ == "__main__":
    # Test all job codes locally
    print("🧪 Testing custom jobs locally...")
    
    for job_name, job_code in JOB_TYPES.items():
        print(f"\n🔧 Testing {job_name}...")
        try:
            # Create safe execution environment
            safe_globals = {'result': None}
            exec(job_code, safe_globals)
            result = safe_globals.get('result', 'No result')
            print(f"✅ {job_name}: {str(result)[:100]}...")
        except Exception as e:
            print(f"❌ {job_name} failed: {e}")
    
    print(f"\n📊 Available jobs: {list_available_jobs()}")
