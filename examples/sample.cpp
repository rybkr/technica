#include <iostream>
#include <vector>

int main() {
    const std::vector<int> readings{12, 18, 24};
    int total = 0;

    for (const auto reading : readings) {
        total += reading;
    }

    std::cout << "Total: " << total << '\n';
    return 0;
}
