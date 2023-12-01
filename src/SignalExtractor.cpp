#include <random>
#include "SignalExtractor.h"
#include <fmt/core.h>
#include <TH1.h>

SignalExtractor::SignalExtractor() { 
    fmt::print("SignalExtractor created at {}\n", (void*) this);
}

SignalExtractor::SignalExtractor(const double scaling, const Range scale_range) :
     m_scale_range{scale_range}, m_scaling{scaling}
{
    //fmt::print("SignalExtractor created at {}\n", (void*) this);
}

SignalExtractor::~SignalExtractor() { 
    //fmt::print("SignalExtractor destroyed at {}\n", (void*) this);
}

auto SignalExtractor::get_scaling() const -> double {
    return m_scaling;
}
auto SignalExtractor::get_scale_range() const -> Range {
    return m_scale_range;
}

auto SignalExtractor::set_scaling(const double value) -> void {
    m_scaling = value;
}

auto SignalExtractor::set_scale_range(const Range value) -> void {
    m_scale_range = value;
}

auto SignalExtractor::extract(const TH1D& fg, const TH1D& bg) const -> std::pair<TH1D, TH1D> {
    const auto bin_range = std::array<int, 2>{
        fg.GetXaxis()->FindBin(m_scale_range[0]), 
        fg.GetXaxis()->FindBin(m_scale_range[1]) - 1
    };

    const auto fg_integral = fg.Integral(bin_range[0], bin_range[1]);
    const auto bg_integral = bg.Integral(bin_range[0], bin_range[1]);
    const auto scale = fg_integral / bg_integral * m_scaling;

    static auto gen = std::mt19937{};
    auto dist = std::uniform_int_distribution<int>(0, 1000); 
    const auto id = dist(gen);

    auto scaled_bg = bg * scale;
    scaled_bg.SetDirectory(nullptr);
    scaled_bg.SetName(fmt::format("signal_{}", id).c_str());

    auto signal = fg - scaled_bg;
    signal.SetDirectory(nullptr);
    signal.SetName(fmt::format("scaled_bg_{}", id).c_str());

    return {signal, scaled_bg};
}
