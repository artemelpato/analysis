#include "SignalExtractor.h"
#include <fmt/core.h>
#include <TH1.h>

SignalExtractor::SignalExtractor() { 
    fmt::print("SignalExtractor created at {}\n", (void*) this);
}

SignalExtractor::SignalExtractor(const double scaling, const Range scale_range) :
     m_scale_range{scale_range}, m_scaling{scaling}
{
    fmt::print("SignalExtractor created at {}\n", (void*) this);
}

SignalExtractor::~SignalExtractor() { 
    fmt::print("SignalExtractor destroyed at {}\n", (void*) this);
}

auto SignalExtractor::scaling() const -> double {
    return m_scaling;
}
auto SignalExtractor::scale_range() const -> Range {
    return m_scale_range;
}

auto SignalExtractor::scaling() -> double& { 
    return m_scaling;
}

auto SignalExtractor::scale_range() -> Range& {
    return m_scale_range;
}

auto SignalExtractor::extract(const TH1D& fg, const TH1D& bg) const -> std::pair<TH1D, TH1D> {
    const auto bin_range = std::array<int, 2>{
        fg.GetXaxis()->FindBin(m_scale_range[0]), 
        fg.GetXaxis()->FindBin(m_scale_range[1]) - 1
    };

    const auto fg_integral = fg.Integral(bin_range[0], bin_range[1]);
    const auto bg_integral = bg.Integral(bin_range[0], bin_range[1]);
    const auto scale = fg_integral / bg_integral * m_scaling;

    auto scaled_bg = bg * scale;
    scaled_bg.SetDirectory(nullptr);
    scaled_bg.SetName("scaled_bg");

    auto signal = fg - scaled_bg;
    signal.SetDirectory(nullptr);
    signal.SetName("signal");

    return {signal, scaled_bg};
}
