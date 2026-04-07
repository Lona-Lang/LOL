#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <list>
#include <string_view>
#include <vector>

namespace {

constexpr std::size_t kCount = 1'000'000;

struct Measure {
    std::uint64_t insert_us;
    std::uint64_t query_us;
    std::uint64_t update_us;
    std::uint64_t delete_us;
    std::uint64_t checksum;
};

using Clock = std::chrono::steady_clock;

std::uint64_t elapsed_us(Clock::time_point start) {
    const auto delta = std::chrono::duration_cast<std::chrono::microseconds>(Clock::now() - start);
    return static_cast<std::uint64_t>(delta.count());
}

Measure run_vec(std::size_t count) {
    std::vector<std::uint64_t> values;
    values.reserve(count);

    auto start = Clock::now();
    for (std::size_t index = 0; index < count; ++index) {
        values.push_back(static_cast<std::uint64_t>(index));
    }
    const auto insert_us = elapsed_us(start);

    std::uint64_t query_sum = 0;
    start = Clock::now();
    for (std::size_t index = 0; index < values.size(); ++index) {
        query_sum += values[index];
    }
    const auto query_us = elapsed_us(start);

    std::uint64_t update_sum = 0;
    start = Clock::now();
    for (std::size_t index = 0; index < values.size(); ++index) {
        values[index] += 1;
        update_sum += values[index];
    }
    const auto update_us = elapsed_us(start);

    std::uint64_t delete_sum = 0;
    start = Clock::now();
    while (!values.empty()) {
        delete_sum += values.back();
        values.pop_back();
    }
    const auto delete_us = elapsed_us(start);

    return Measure{
        .insert_us = insert_us,
        .query_us = query_us,
        .update_us = update_us,
        .delete_us = delete_us,
        .checksum = query_sum + update_sum + delete_sum,
    };
}

Measure run_list(std::size_t count) {
    std::list<std::uint64_t> values;

    auto start = Clock::now();
    for (std::size_t index = 0; index < count; ++index) {
        values.push_back(static_cast<std::uint64_t>(index));
    }
    const auto insert_us = elapsed_us(start);

    std::uint64_t query_sum = 0;
    start = Clock::now();
    for (const auto value : values) {
        query_sum += value;
    }
    const auto query_us = elapsed_us(start);

    std::uint64_t update_sum = 0;
    start = Clock::now();
    for (auto& value : values) {
        value += 1;
        update_sum += value;
    }
    const auto update_us = elapsed_us(start);

    std::uint64_t delete_sum = 0;
    start = Clock::now();
    while (!values.empty()) {
        delete_sum += values.front();
        values.pop_front();
    }
    const auto delete_us = elapsed_us(start);

    return Measure{
        .insert_us = insert_us,
        .query_us = query_us,
        .update_us = update_us,
        .delete_us = delete_us,
        .checksum = query_sum + update_sum + delete_sum,
    };
}

void print_measure(std::string_view name, std::size_t count, const Measure& measure) {
    std::cout
        << name
        << " count=" << count
        << " insert_us=" << measure.insert_us
        << " query_us=" << measure.query_us
        << " update_us=" << measure.update_us
        << " delete_us=" << measure.delete_us
        << " checksum=" << measure.checksum
        << '\n';
}

}  // namespace

int main() {
    print_measure("c++ vec", kCount, run_vec(kCount));
    print_measure("c++ list", kCount, run_list(kCount));
    return EXIT_SUCCESS;
}
