#ifndef __SIGNAL_EXTRACTOR_H__
#define __SIGNAL_EXTRACTOR_H__

#include <array>
#include <fmt/core.h>
#include <TH1.h>
#include <tuple>

class SignalExtractor {
public:
    using Range = std::vector<double>;

    SignalExtractor();
    SignalExtractor(const double scaling, const Range scale_range, const Range aux_scale_range);
    ~SignalExtractor();

    auto set_scaling(const double value);
    auto set_scale_ranges(const Range value, const Range aux_range);

    auto get_scaling() const -> double;
    auto get_scale_ranges() const -> std::vector<Range>;

    auto extract(const TH1D& fg, const TH1D& bg) const -> std::pair<TH1D, TH1D>;

private:
    Range m_scale_range{0, 0};
    Range m_aux_scale_range{0, 0};
    double m_scaling{};
};

#endif // __SIGNAL_EXTRACTOR_H__
