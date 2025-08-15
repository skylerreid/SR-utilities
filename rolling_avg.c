#include <stddef.h>

__declspec(dllexport)
void rolling_average(const double* data, size_t len, size_t window, double* out) {
    if (window == 0 || window > len) return;

    for (size_t i = 0; i <= len - window; i++) {
        double sum = 0.0;
        for (size_t j = 0; j < window; j++) {
            sum += data[i + j];
        }
        out[i] = sum / window;
    }
}