import math

def estimate_error_bounds(digits):
    # Constants
    C = 640320
    C3_OVER_24 = C**3 // 24
    DIGITS_PER_TERM = math.log10(C3_OVER_24/6/2/6)
    MAX_PRECISION_LOSS = 0.5  # Assuming a maximum precision loss of 1/2 per least significant bit

    # Calculate the number of iterations needed to reach the desired precision
    N = int(digits / DIGITS_PER_TERM + 1)

    # Estimate the maximum error due to the accuracy of the algorithm
    algorithm_error = digits - N * DIGITS_PER_TERM

    # Estimate the maximum error due to numerical precision
    # Assuming a multiplication operation for each iteration
    precision_error = N * MAX_PRECISION_LOSS

    # Calculate the total error bound by adding both errors
    total_error_bound = algorithm_error + precision_error

    return total_error_bound

# Example usage:
digits = 12
error_bound = estimate_error_bounds(digits)
print(f"Estimated error bound for {digits} decimal places: {error_bound}")
