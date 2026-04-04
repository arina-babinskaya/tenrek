// функции генерировала с помощью нейронки, так как данном этапе важно убедиться, что всё хотя бы не ломается


bool isPrime(long long n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    
    if (n % 2 == 0 || n % 3 == 0) return false;
    
    for (long long i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return false;
        }
    }
    return true;
}

void printStats(int count, float* numbers, double* avg, float* min_val, float* max_val) {
    *avg = 0.0;
    *min_val = numbers[0];
    *max_val = numbers[0];
    
    for (int i = 0; i < count; i++) {
        *avg += numbers[i];
        
        if (numbers[i] < *min_val) {
            *min_val = numbers[i];
        }
        if (numbers[i] > *max_val) {
            *max_val = numbers[i];
        }
    }
    
    *avg /= count;
}

